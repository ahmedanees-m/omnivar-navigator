# Compute topology & local <-> VM workflow

Two machines, a strict division of labor, and a **Docker-only rule on the server**.

| | Laptop (dev) | VM `sjt418scope025` (compute + host) |
|---|---|---|
| Spec | 2.5 GHz, 8 GB RAM | 24 cores, 64 GB RAM, RTX A4000 16 GB GPU, Ubuntu 22.04 |
| Role | write code, lint, unit tests on tiny fixtures, git, author Docker*files* | all heavy work: full data, feature extraction, LLM orchestration, validation runs, hosting the web app |
| Never | run full pipelines, hold real data | install software on the host (Docker images only) |

## Workflow

1. Develop + unit-test locally on small fixtures; push to GitHub.
2. On the VM, pull the repo and run everything via `docker compose` (images built
   on the VM or pulled from GHCR).
3. Automate VM control from the laptop with **paramiko** over SSH (`deploy/remote.py`).

## Data sync (SFTP, not rclone)

Reference data, checkpointed Parquet, trained models, and versioned backups live
on **both** the VM (`/home/anees_22phd0670/omnivar-navigator/data/`) and the `G:`
drive (`G:\My Drive\OmniVar\data\`). They are kept in parity with **SFTP**
(`deploy/remote.py: put/get`); we deliberately do **not** use rclone.

Heavy reference data is bind-mounted **read-only** into containers.

## VM specifics (verified June 2026)

- Docker 29.1.3; GPU RTX A4000 (16 GB).
- Disk: ~468 GB total; keep an eye on free space (large model images already
  present for sibling projects). Prefer the `G:` drive for cold archives.
- **Do not touch sibling projects on the VM** (pen-stack, genome-atlas, netmhc,
  ProteinMPNN, boltz1, mhc*, …). OmniVar work stays under `omnivar-navigator/`.

## LLM

The reasoning/soft-task LLM is **cloud Nemotron** (NVIDIA NIM, OpenAI-compatible
at `https://integrate.api.nvidia.com/v1`), not a self-hosted Ollama model. Default
model: **`nvidia/llama-3.3-nemotron-super-49b-v1`** (Nemotron Super 49B, free
build.nvidia.com catalog tier — free credits + rate caps, not metered), overridable
via `NEMOTRON_MODEL`. See `llm/gateway.py`. The key is read from `NVIDIA_API_KEY`.

## Security

Secrets (VM auth, API keys) come from environment variables, never from code or
git. Connecting helper: set `VM_HOST`, `VM_USER`, and either an SSH key
(`VM_KEY`) or `VM_PASSWORD`. Key-based auth is preferred; see `docs/SECURITY.md`.
