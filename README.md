# CO5085: Deep Learning and its Applications in Computer Vision

Coursework repository for **HK261**: four exercises (**E1-E4**) and two assignments
(**A1-A2**) covering deep learning for computer vision, from basic classifiers to
transformers, sequence models, generative models, and a self-chosen research topic.

Every experiment is **config-driven**: a YAML file describes the data, model,
optimizer, loss, metrics, and handlers, and a single command trains or evaluates it.
Results are written up as posts on a report site in `docs/`.

Report site: https://tronglh241.github.io/co5085_excersises_and_assignments

## What's inside

| ID | Topic | What we compare |
|----|-------|-----------------|
| E1 | Image classification on a small set (MNIST / Fashion-MNIST / CIFAR-10) | Softmax vs MLP vs CNN: accuracy, capacity, error cases |
| E2 | Multi-Head Self-Attention, from scratch and with PyTorch modules | Several tokenizations (patch, pixel/row, CNN-stem, CLS + patches) |
| E3 | Sequence models on images as sequences (e.g. MNIST rows) | LSTM and GRU vs a feed-forward / CNN baseline |
| E4 | Generative models on a small MNIST-like set | VAE, GAN, Diffusion: sample quality, latent space, compute |
| A1 | Self-chosen large image dataset | CNN vs Transformer; from scratch vs pretrained; frozen, partially frozen, full finetune |
| A2 | Self-chosen topic (detection, segmentation, ...) | Working pipeline plus analysis of one related paper |

## How it works

- **[ignite](https://github.com/pytorch/ignite)** provides the training engine, metrics, and handlers.
- **[flame](https://github.com/tronglh241/flame)** builds on ignite and turns a YAML config into a full train or evaluation run (engine, metrics, checkpointing, early stopping, TensorBoard logging).
- Our own code lives in `datasets/`, `models/`, and `handlers/`, and configs in `configs/` reference it. The two libraries are git submodules in `third_party/` and are never edited; fixes go in our code or in config.
- Training writes TensorBoard events to `logs/` and checkpoints to `checkpoints/`. Scripts turn those logs into CSVs and figures, which are used in the posts under `docs/`.

## Prerequisites

Everything runs **inside a Docker container**, so the host needs only:

- **Docker Engine** or Docker Desktop: [installation instructions](https://docs.docker.com/engine/install/)
- **Docker Compose** (included with Docker Desktop): [installation instructions](https://docs.docker.com/compose/install/)
- For GPU mode only: the **NVIDIA Container Toolkit**: [installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). CPU mode needs no GPU.

No Python or Ruby toolchain is required on the host.

## Quickstart

```bash
git clone --recurse-submodules https://github.com/tronglh241/co5085_excersises_and_assignments
cd co5085_excersises_and_assignments
# already cloned without submodules?  git submodule update --init --recursive

cp .env.example .env         # once; set ids from `id -u` / `id -g`
scripts/shell.sh [gpu|cpu]   # default gpu
```

All commands in the sections below run inside this container shell.

## Usage

### Train and evaluate

Pattern:

```bash
flame run configs/<exercise>/<train|test>/<config_name>.yml
```

`<exercise>` is `e1`-`e4` or `a1`-`a2`. The same command trains or evaluates,
depending on whether the config is under `train/` or `test/`.

Example (E1, softmax classifier):

```bash
flame run configs/e1/train/softmax.yml   # train
flame run configs/e1/test/softmax.yml    # evaluate
```

TensorBoard events are written to `logs/` and checkpoints to `checkpoints/`.

### Inspect results

```bash
scripts/tensorboard.sh [logdir]                                 # live curves at localhost:6006 (default: logs/)
python scripts/extract_tensorboard.py [--logdir <run|parent>]   # per-run metrics.csv for plotting
```

`--logdir` is optional. It accepts a single run directory or a parent directory
containing several runs.

### Docs site

```bash
scripts/serve.sh   # live preview at localhost:4000/co5085_excersises_and_assignments/
scripts/build.sh   # CI gate; run before every push
```

### Code style

```bash
scripts/lint.sh    # isort + flake8 over datasets/ handlers/ models/ scripts/
```

## Layout

```text
configs/{e,a}N/{train,test}/<name>.yml      flame experiment configs
datasets/{e,a}N/                            torch datasets
handlers/                                   our ignite handlers
models/{e,a}N/                              torch modules
scripts/{e,a}N/                             runnable helpers
scripts/                                    bash script helpers
docs/                                       Report site
third_party/                                flame, ignite (git submodules, read-only)
data/ checkpoints/ logs/                    runtime artifacts, gitignored: never commit
```
