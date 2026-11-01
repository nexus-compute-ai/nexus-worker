import asyncio
import json
import logging
import time
import urllib.parse
from typing import Dict, Any, List, Optional
import httpx

from nexus_worker.hardware import detect_hardware
from nexus_worker.engine import InferenceEngineClient

logger = logging.getLogger("nexus_worker")

class WorkerDaemon:
    def __init__(
        self,
        node_token: str,
        coordinator_url: str = "https://nexus-compute.pages.dev",
        ollama_url: str = "http://localhost:11434",
        vllm_url: str = "http://localhost:8000",
        emulate: bool = False,
        prompt_price: float = 0.20,
        completion_price: float = 0.40
    ):
        self.node_token = node_token
        # Normalize coordinator URL
        url = coordinator_url.rstrip("/")
        if url.startswith("ws://"):
            url = url.replace("ws://", "http://", 1)
        elif url.startswith("wss://"):
            url = url.replace("wss://", "https://", 1)
        # Remove trailing path if old /api/v1/ws/worker path was passed
        if "/api/v1/ws/worker" in url:
            url = url.replace("/api/v1/ws/worker", "")
        self.coordinator_url = url

        self.prompt_price = prompt_price
        self.completion_price = completion_price
        self.engine = InferenceEngineClient(ollama_url=ollama_url, vllm_url=vllm_url, emulate=emulate)
        self.running = False

    async def start(self):
        self.running = True

        # 1. Detect hardware
        hw = detect_hardware()
        print(f"\n[NexusCompute Worker] Detected Hardware: {hw['gpu_name']} ({hw['vram_mb']} MB VRAM)", flush=True)

        # 2. Discover local models
        models = self.engine.discover_models()
        print(f"[NexusCompute Worker] Engine: {self.engine.active_engine.upper()} | Serving {len(models)} model(s): {', '.join(models)}", flush=True)

        # 3. Benchmark tokens/sec
        print("[NexusCompute Worker] Running startup synthetic benchmark probe...", flush=True)
        bench_speed = await self.engine.run_benchmark()
        print(f"[NexusCompute Worker] Benchmark Result: {bench_speed} tokens/second", flush=True)

        models_param = ",".join(models) if models else "llama3:8b,deepseek-r1:7b,mistral:7b"
        headers = {
            "Authorization": f"Bearer {self.node_token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 NexusWorker/1.0",
        }

        print(f"[NexusCompute Worker] Connecting to Cloudflare Edge Coordinator: {self.coordinator_url}", flush=True)
        print("[NexusCompute Worker] Node is ONLINE and actively polling for AI inference jobs...\n", flush=True)

        backoff = 2
        async with httpx.AsyncClient(
            headers=headers,
            timeout=httpx.Timeout(connect=10.0, read=35.0, write=10.0, pool=10.0)
        ) as client:
            while self.running:
                try:
                    poll_url = (
                        f"{self.coordinator_url}/api/v1/jobs/poll"
                        f"?models={urllib.parse.quote(models_param)}"
                        f"&gpu_name={urllib.parse.quote(hw['gpu_name'])}"
                        f"&vram_mb={hw['vram_mb']}"
                        f"&tokens_per_sec={bench_speed}"
                    )

                    resp = await client.get(poll_url)
                    if resp.status_code == 200:
                        backoff = 2  # Reset on successful network request
                        data = resp.json()
                        job_id = data.get("job_id")

                        if job_id:
                            # Job acquired! Process and stream tokens
                            await self._process_job(client, data)
                        else:
                            # Timeout / heartbeat ack, continue immediately
                            pass

                    elif resp.status_code == 401:
                        print(f"[NexusCompute Worker] [ERROR] Authentication failed! Invalid node token: {self.node_token[:12]}...", flush=True)
                        await asyncio.sleep(10)
                    else:
                        print(f"[NexusCompute Worker] Polling returned status {resp.status_code}. Retrying...", flush=True)
                        await asyncio.sleep(backoff)
                        backoff = min(20, backoff * 1.5)

                except (httpx.ReadTimeout, httpx.ConnectTimeout):
                    # Standard long-poll expiration, loop immediately
                    continue
                except httpx.RequestError as e:
                    print(f"[NexusCompute Worker] Connection error ({type(e).__name__}). Reconnecting in {backoff}s...", flush=True)
                    await asyncio.sleep(backoff)
                    backoff = min(20, backoff * 1.5)
                except Exception as e:
                    print(f"[NexusCompute Worker] Unexpected error: {e}", flush=True)
                    await asyncio.sleep(backoff)

    async def _process_job(self, client: httpx.AsyncClient, job_data: dict):
        job_id = job_data.get("job_id")
        model = job_data.get("model")
        messages = job_data.get("messages", [])
        temperature = job_data.get("temperature", 0.7)
        max_tokens = job_data.get("max_tokens", 512)

        print(f"\n[NexusCompute Worker] >> [CLAIMED] Job {job_id[:8]} for model '{model}'", flush=True)
        start_time = time.time()
        seq = 0
        prompt_tokens = 15
        completion_tokens = 0
        full_text_chunks = []

        try:
            async for chunk in self.engine.stream_chat(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            ):
                if chunk["type"] == "chunk":
                    seq += 1
                    completion_tokens += 1
                    delta = chunk["delta"]
                    full_text_chunks.append(delta)

                    # POST chunk to Cloudflare Edge
                    stream_url = f"{self.coordinator_url}/api/v1/jobs/{job_id}/stream"
                    try:
                        await client.post(stream_url, json={"seq": seq, "delta": delta})
                    except Exception as ex:
                        logger.warning(f"Failed to post chunk {seq}: {ex}")

                elif chunk["type"] == "done":
                    prompt_tokens = chunk.get("prompt_tokens", 15)
                    completion_tokens = chunk.get("completion_tokens", completion_tokens)
                    break

            latency_ms = int((time.time() - start_time) * 1000)
            full_response = "".join(full_text_chunks)
            # Settle completion
            complete_url = f"{self.coordinator_url}/api/v1/jobs/{job_id}/complete"
            await client.post(complete_url, json={
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "latency_ms": latency_ms,
                "response_payload": full_response,
            })
            print(f"[NexusCompute Worker] << [COMPLETED] Job {job_id[:8]} in {latency_ms}ms ({completion_tokens} tokens streamed, payout recorded)!\n", flush=True)

        except Exception as e:
            print(f"[NexusCompute Worker] !! [ERROR] Job {job_id[:8]} failed: {e}", flush=True)
            try:
                await client.post(f"{self.coordinator_url}/api/v1/jobs/{job_id}/stream", json={
                    "seq": seq + 1,
                    "delta": f"\n[Inference Error: {str(e)}]"
                })
                await client.post(f"{self.coordinator_url}/api/v1/jobs/{job_id}/complete", json={
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "error": str(e)
                })
            except Exception:
                pass
