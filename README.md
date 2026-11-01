# ⚡ NexusWorker (`nexus-worker`)

[![PyPI](https://img.shields.io/pypi/v/nexus-worker.svg)](https://pypi.org/project/nexus-worker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Decentralized AI](https://img.shields.io/badge/Network-NexusCompute%20Edge-teal.svg)](https://nexus-compute.pages.dev)

**NexusWorker** is the open-source provider daemon for the **NexusCompute** decentralized AI inference network.

Run this lightweight daemon on your laptop (Apple Silicon MacBook, Windows RTX laptop, or Linux notebook), homelab rig, or cloud GPU server to monetize your idle graphics cards and compute power by serving inference tokens for open-source LLMs (Llama 3, DeepSeek-R1, Mistral, Qwen).

---

## 🔒 Security & Privacy (Outbound-Only)

NexusWorker was designed from the ground up for strict security:

* **Zero Inbound Ports**: The daemon initiates an **outbound-only** connection to the NexusCompute coordinator. You **never** need to configure port forwarding, open firewall rules, or expose a public IP.
* **Completely Sandboxed**: The worker only communicates with your local inference engine (e.g. Ollama or vLLM) over localhost (`127.0.0.1`).
* **100% Open Source**: Full transparency—inspect every line of code before running.

---

## 🚀 Laptop & Desktop Quickstart Guide

### 1. Requirements

* **OS**: macOS (Apple Silicon M1/M2/M3/M4 or Intel), Windows 10/11, or Linux
* **Python**: 3.9 or higher
* **Inference Engine**: [Ollama](https://ollama.ai) (recommended for 1-click local setup) or [vLLM](https://github.com/vllm-project/vllm).
* **Hardware**: Any modern GPU (NVIDIA RTX 3060/3080/4090, Apple Silicon unified memory), or CPU with emulation support.

---

### 2. Step-by-Step Setup

#### Step 1: Install Ollama & Pull a Model
Ollama runs natively on Mac, Windows, and Linux:
1. Download & install from **[ollama.com/download](https://ollama.com/download)**.
2. Open your terminal and pull an open-source model:
   ```bash
   ollama run llama3:8b
   ```
   *(You can also use `deepseek-r1:7b` or `mistral:7b`)*.

#### Step 2: Install NexusWorker from PyPI
Install the official provider daemon using pip:
```bash
pip install nexus-worker
```

Verify your hardware and local model detection:
```bash
nexus-worker info
```

Example output:
```text
============================================================
              NEXUSCOMPUTE HARDWARE DETECTOR                
============================================================
• GPU: Apple M3 Max / NVIDIA GeForce RTX 4090
• VRAM: 36,864 MB
• Backend Engine: Ollama (http://127.0.0.1:11434)
• Discovered Models:
    - llama3:8b
    - deepseek-r1:7b
============================================================
```

#### Step 3: Register Your Node on the Dashboard
1. Go to **[nexus-compute.pages.dev](https://nexus-compute.pages.dev)**.
2. Sign in and open the **Provider Node** tab.
3. Type a name for your machine (e.g., `MacBook-Pro-M3` or `Alienware-RTX4080`) and click **Add Node**.
4. Copy your node token (`nx-node-...`).

#### Step 4: Connect & Start Earning
Start the worker daemon:
```bash
nexus-worker start --token nx-node-YOUR_TOKEN_HERE
```

That's it! Your laptop is now connected to the decentralized inference mesh:
* The node will automatically appear **online** in your dashboard.
* When consumers run queries on your served model, your node streams tokens and 90% of token fees are automatically credited to your wallet in real time.

---

## 💡 Testing Without Downloading Large Models (Emulation Mode)

If you want to test connecting your node immediately before downloading gigabytes of model weights, run with the `--emulate` flag:

```bash
nexus-worker start --token nx-node-YOUR_TOKEN_HERE --emulate
```

The daemon will simulate high-performance streaming token output (~45 tok/s), allowing you to verify coordinator connectivity, heartbeat telemetry, and testnet payouts right away.

---

## 🛠️ CLI Reference

```bash
nexus-worker [OPTIONS] COMMAND [ARGS]...

Commands:
  info   Display local GPU hardware specifications and discovered AI engines.
  start  Start the provider daemon and connect outbound to the NexusCompute network.
```

### Options for `nexus-worker start`:
* `--token, -t TEXT`: Provider node token from dashboard *(required)*.
* `--coordinator, -c TEXT`: Coordinator URL (default: `https://nexus-compute.pages.dev`).
* `--ollama-url TEXT`: Local Ollama HTTP endpoint (default: `http://localhost:11434`).
* `--vllm-url TEXT`: Local vLLM HTTP endpoint (default: `http://localhost:8000`).
* `--emulate`: Run in emulation mode (simulates GPU streaming).
* `--prompt-price FLOAT`: Custom price per 1M prompt tokens in credits (default: `0.20`).
* `--completion-price FLOAT`: Custom price per 1M completion tokens in credits (default: `0.40`).

---

## 📄 License

Distributed under the **MIT License**.
