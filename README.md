# ⚡ NexusWorker (`nexus-worker`)

[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Decentralized AI](https://img.shields.io/badge/Mesh-Decentralized%20Inference-teal.svg)](https://nexuscompute.ai)

**NexusWorker** is the open-source provider daemon for the **NexusCompute** decentralized AI inference network.

Run this lightweight daemon on your PC, mining rig, or server to monetize your idle graphics cards (NVIDIA, AMD, Apple Silicon) by serving inference tokens for open-source LLMs (Llama 3, DeepSeek-R1, Mistral).

---

## 🔒 Security & Privacy (Outbound-Only)

NexusWorker was designed from the ground up for strict security:

* **Zero Inbound Ports**: The daemon initiates an **outbound-only** encrypted WebSocket connection to the NexusCompute coordinator. You **never** need to configure port forwarding, open firewall rules, or expose a public IP.
* **Completely Sandboxed**: The worker only communicates with your local inference engine (e.g. Ollama or vLLM) over localhost (`127.0.0.1`).
* **100% Open Source**: Full transparency—inspect every line of code before running.

---

## 🚀 Quickstart

### 1. Requirements

* **OS**: Linux, Windows, or macOS
* **Python**: 3.9 or higher
* **Inference Engine**: [Ollama](https://ollama.ai) (recommended for 1-click setup) or [vLLM](https://github.com/vllm-project/vllm).
* **Hardware**: Any modern GPU with 6GB+ VRAM (e.g. RTX 3060/3080/4090, Apple M-series), or CPU in emulation mode.

---

### 2. Installation

Clone and install in a Python virtual environment:

```bash
git clone https://github.com/nexus-compute-ai/nexus-worker.git
cd nexus-worker

# Create and activate virtual environment
python -m venv .venv
# On Windows:
.\.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install package
pip install -e .
```

---

### 3. Check Detected Hardware

Verify that your GPU and local models are recognized:

```bash
nexus-worker info
```

Example output:
```text
============================================================
              NEXUSCOMPUTE HARDWARE DETECTOR                
============================================================
• GPU: NVIDIA GeForce RTX 4090
• VRAM: 24,576 MB
• Backend Engine: Ollama (http://127.0.0.1:11434)
• Discovered Models:
    - llama3:8b
    - deepseek-r1:7b
    - mistral:7b
============================================================
```

---

### 4. Connect to Network & Earn

Get your node token from the **Provider Dashboard** on NexusCompute, then start the daemon:

```bash
nexus-worker start --token nx-node-YOUR_TOKEN_HERE
```

#### CLI Options:
* `--token TEXT`: Your unique node authorization token *(required)*.
* `--coordinator TEXT`: Coordinator WebSocket URL (default: `ws://127.0.0.1:8000/api/v1/ws/worker`).
* `--engine [auto|ollama|vllm|emulate]`: Local inference engine (default: `auto`).
* `--emulate`: Run in emulation mode for development without downloading weights.

```bash
# Example with custom coordinator and auto-discovery
nexus-worker start --token nx-node-0a0a3b29ed4e323af354549a6681821a1b75157e
```

---

## 🛠️ Supported Engines

1. **Ollama (Recommended)**: Pull models via `ollama pull llama3:8b`. NexusWorker will auto-detect active models and advertise them to the coordinator.
2. **vLLM (High-Throughput)**: Launch with OpenAI-compatible API (`--port 8000`).
3. **Emulation Engine**: Built-in mock tokenizer and streaming generator for rapid testing.

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more information.
