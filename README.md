# ⚡ Become a Compute Provider with NexusWorker

[![PyPI](https://img.shields.io/pypi/v/nexus-worker.svg)](https://pypi.org/project/nexus-worker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-emerald.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Provider Portal](https://img.shields.io/badge/Provider%20Portal-NexusCompute-teal.svg)](https://nexus-compute.pages.dev)

> **Monetize your idle GPU & compute power by serving open-source AI inference on the NexusCompute decentralized network.**

Whether you have a laptop (Apple Silicon MacBook M1/M2/M3/M4, Windows RTX laptop, or Linux notebook), a gaming desktop (NVIDIA RTX 3060/4080/4090), a homelab rig, or a dedicated cloud GPU cluster, **NexusWorker** enables you to earn passive revenue by serving inference requests for open LLMs like **Llama 3**, **DeepSeek-R1**, **Mistral**, and **Qwen**.

---

## 💡 Why Provide Compute on NexusCompute?

* 💰 **Passive Income**: 90% of all token fees from consumer queries are automatically credited to your provider wallet in real time.
* 🔒 **100% Secure & Outbound-Only**: Zero inbound open ports, no port-forwarding, and no router configuration needed. The daemon connects outbound to Cloudflare Edge.
* 🛡️ **Completely Sandboxed**: Only interacts with your local inference backend (Ollama / vLLM) over localhost (`127.0.0.1`).
* ⚡ **1-Minute Setup**: Install in a single command with `pip install nexus-worker`.
* 🖥️ **Full Cross-Platform Support**: macOS (Apple Silicon unified memory & Intel), Windows 10/11, and Linux.
* ⏸️ **You're in Control**: Start, pause, or stop whenever you need your machine for gaming or work (`Ctrl + C`).

---

## 🚀 Provider Quickstart Guide (Under 3 Minutes)

### Requirements:
* **OS**: macOS (Apple Silicon M-series or Intel), Windows 10/11, or Linux
* **Python**: 3.9 or higher
* **Inference Engine**: [Ollama](https://ollama.ai) (recommended for 1-click local setup) or [vLLM](https://github.com/vllm-project/vllm)
* **Hardware**: Any modern GPU (NVIDIA RTX 2060/3060/4090, Apple Silicon unified memory), or CPU with emulation support

---

### Step 1: Install Ollama & Pull a Model
Ollama runs natively on Mac, Windows, and Linux:
1. Download & install from **[ollama.com/download](https://ollama.com/download)**.
2. Open your terminal and pull an open-source model:
   ```bash
   ollama run llama3:8b
   ```
   *(You can also serve `deepseek-r1:7b` or `mistral:7b`)*.

---

### Step 2: Install NexusWorker from PyPI
Install the official provider daemon using pip:
```bash
pip install nexus-worker
```

Verify your hardware and local model detection:
```bash
nexus-worker info
```

*Example output:*
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

---

### Step 3: Register Your Node on the Dashboard
1. Go to **[nexus-compute.pages.dev](https://nexus-compute.pages.dev)**.
2. Sign in and open the **Provider Node** tab.
3. Type a name for your machine (e.g., `MacBook-Pro-M3` or `Alienware-RTX4080`) and click **Add Node**.
4. Copy your unique node token (`nx-node-...`).

---

### Step 4: Connect & Start Earning
Start the worker daemon:
```bash
nexus-worker start --token nx-node-YOUR_TOKEN_HERE
```

That's it! Your machine is now connected to the decentralized inference mesh:
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

## 🛠️ CLI Reference for Providers

```bash
nexus-worker [OPTIONS] COMMAND [ARGS]...

Commands:
  info   Display local GPU hardware specifications and discovered AI engines.
  start  Start the provider daemon and connect outbound to the NexusCompute network.
```

### Options for `nexus-worker start`:
| Flag | Default | Description |
| :--- | :--- | :--- |
| `--token, -t` *(required)* | - | Provider node token from dashboard |
| `--coordinator, -c` | `https://nexus-compute.pages.dev` | Coordinator edge URL |
| `--ollama-url` | `http://localhost:11434` | Local Ollama HTTP endpoint |
| `--vllm-url` | `http://localhost:8000` | Local vLLM HTTP endpoint |
| `--engine` | `auto` | Backend engine selection (`auto`, `ollama`, `vllm`, `emulate`) |
| `--poll-interval` | `1.0` | Polling heartbeat interval (seconds) |
| `--emulate` | `false` | Run in emulation mode (simulates GPU streaming) |

**Example with custom coordinator or endpoint:**
```bash
nexus-worker start --token nx-node-0a0a3b29ed4e323af354549a6681821a1b75157e
```

---

## ❓ Frequently Asked Questions (FAQ) for Providers

<details>
<summary><b>Do I need to open any firewall ports or configure port-forwarding on my router?</b></summary>
<br>
<b>No.</b> NexusWorker uses outbound HTTP/2 long-polling to communicate with the coordinator edge. Because all network traffic is initiated outbound from your computer, it works behind any home router, NAT, corporate firewall, or VPN without any configuration.
</details>

<details>
<summary><b>What happens when I want to play games or use my machine?</b></summary>
<br>
Simply press <code>Ctrl + C</code> in the terminal where <code>nexus-worker</code> is running. The daemon will gracefully disconnect and notify the coordinator. Whenever you are done with your GPU, run <code>nexus-worker start --token ...</code> to resume earning.
</details>

<details>
<summary><b>What hardware is required?</b></summary>
<br>
Any GPU with at least 6 GB VRAM (e.g. NVIDIA RTX 2060/3060/4060/4090, AMD Radeon 6000/7000 series, or Apple Silicon M1/M2/M3/M4 with unified memory). You can also run CPU inference or test using the <code>--emulate</code> flag.
</details>

<details>
<summary><b>How do I track my earnings and node uptime?</b></summary>
<br>
Visit your <a href="https://nexus-compute.pages.dev">Provider Dashboard</a> to view real-time metrics including tokens served, active hours, latency benchmarks, and accrued balance.
</details>

---

## 💻 Developer Installation (From Source)

If you wish to contribute to the open-source provider daemon codebase:

```bash
git clone https://github.com/nexus-compute-ai/nexus-worker.git
cd nexus-worker

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Or .\.venv\Scripts\activate on Windows

# Install in editable mode
pip install -e .
```

---

## 📄 License

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more details.
