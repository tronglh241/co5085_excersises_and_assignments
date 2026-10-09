# Setup Guide

How to get a working environment. For day-to-day commands, see [DEV.md](DEV.md).

**Use Docker unless you cannot.** One image gives an identical environment on every machine: Python 3.12, torch 2.7.1 (cu126), Ruby/Jekyll, TeX Live and lint tools. The manual path covers **experiments only**. Previewing the site and building the report require Docker.

## Contents

- [Docker (recommended)](#docker-recommended)
  - [1. Prerequisites](#1-prerequisites)
  - [2. Clone the repository](#2-clone-the-repository)
  - [3. Configure `.env`](#3-configure-env)
  - [4. Build the images](#4-build-the-images)
  - [5. Verify](#5-verify)
- [Manual (experiments only)](#manual-experiments-only)
  - [1. Prerequisites](#1-prerequisites-1)
  - [2. Clone the repository](#2-clone-the-repository-1)
  - [3. Create the virtual environment](#3-create-the-virtual-environment)
  - [4. Verify](#4-verify)
- [Troubleshooting](#troubleshooting)

## Docker (recommended)

### 1. Prerequisites

- [Docker Engine](https://docs.docker.com/engine/install/) 24+
- [Docker Compose](https://docs.docker.com/compose/install/) v2
- git

To use the GPU (`gpu` service), you also need:

- NVIDIA driver 560+
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html), so containers can access the GPU

No NVIDIA GPU? Skip the two items above and use the `cpu` service.

### 2. Clone the repository

Downloads the code and moves into it.

```bash
git clone https://github.com/tronglh241/co5085_excersises_and_assignments.git
cd co5085_excersises_and_assignments
```

### 3. Configure `.env`

Creates your local environment file. Set `UID` and `GID` to the output of `id -u` and `id -g`, so files written inside the container belong to you instead of root.

```bash
cp .env.example .env
```

Do this once. `.env` is never committed.

### 4. Build the images

Builds the services you need. The first build downloads several GB (CUDA wheels, TeX Live), so slow is normal.

| Service | Use for |
|---|---|
| `gpu` | Experiments and site preview, with a GPU |
| `cpu` | Experiments and site preview, no NVIDIA stack |
| `latex` | Building the report |

```bash
docker compose build <gpu|cpu|latex>
```

Examples:

```bash
docker compose build gpu
docker compose build latex
```

Build only what you will use. For example, if you only build the report, you only need `latex`.

### 5. Verify

Starts a shell in the container and checks that torch is installed and can see the GPU.

```bash
bash scripts/shell/dev.sh <gpu|cpu>
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Expected output: `2.7.1+cu126 True` plus your GPU name. `False` is fine on the `cpu` service.

You are ready. Continue with [DEV.md](DEV.md).

## Manual (experiments only)

Use this only when Docker is unavailable. For the site and the report, use Docker.

### 1. Prerequisites

- Python 3.12 with `venv`
- git
- Optional, for GPU: NVIDIA driver 560+.

### 2. Clone the repository

Downloads the code and moves into it.

```bash
git clone https://github.com/tronglh241/co5085_excersises_and_assignments.git
cd co5085_excersises_and_assignments
```

### 3. Create the virtual environment

Creates an isolated Python environment, activates it, and installs the pinned dependencies.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Verify

Checks that torch is installed and can see the GPU.

```bash
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

Expected output: `2.7.1+cu126 True` plus your GPU name. `False` is fine on a CPU-only machine.

You are ready. Continue with [DEV.md](DEV.md).

## Troubleshooting

| Symptom | Fix |
|---|---|
| Root-owned files in the repo | `UID`/`GID` in `.env` are wrong. Fix them and rebuild. |
| GPU not visible in the container | Check the NVIDIA driver and Container Toolkit, or use the `cpu` service. |
| `cuda.is_available()` is `False` | Expected on CPU-only machines. Otherwise check the driver version (560+). |
| First `docker compose build` is slow | Expected, one-time cost. |
