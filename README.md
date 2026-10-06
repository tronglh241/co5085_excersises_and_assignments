# CO5085: Deep Learning and its Applications in Computer Vision

Coursework repository for **HK261**: three exercises (**E1–E3**) and two
assignments (**A1–A2**) covering deep learning for computer vision, from basic
classifiers to transformers, sequence models, and self-chosen topics.
Full requirements: `exercise.pdf`, `assignment_1.pdf`, `assignment_2.pdf`.

Every experiment is **config-driven**: a YAML file describes the data, model,
and hyperparameters; it is evaluated to Python objects with our own vendored
config loader, and a per-task `train.py` runs an explicit PyTorch training loop
(`forward → loss → backward() → optimizer.step()` — no ignite, no flame, no
`trainer.fit()`). Results are written up in `reports/exercises.pdf` and in posts
on the report site in `docs/`.

Report site: https://tronglh241.github.io/co5085_excersises_and_assignments

## What's inside

| ID | Topic | What we compare |
|----|-------|-----------------|
| E1 | Image classification on a small set (MNIST / Fashion-MNIST / CIFAR-10) | Softmax vs MLP vs CNN: accuracy, capacity, error cases |
| E2 | Multi-Head Self-Attention, from scratch and with PyTorch modules | Several tokenizations (patch, pixel/row, CNN-stem) on the same set |
| E3 | LSTM and GRU on images as sequences | Sequence views + LSTM vs GRU, vs the E1 MLP/CNN baseline |
| A1 | Self-chosen large image dataset | CNN vs Transformer; from scratch vs pretrained; frozen, partially frozen, full finetune |
| A2 | Self-chosen non-classification topic | Working pipeline (≥2 variants) plus analysis of one related paper |

## How it works

- Each task lives in its own directory (`E1/`, `E2/`, …) with `configs/*.yaml`,
  `datasets/`, `models/`, `train.py`, `evaluate.py`, and `scripts/`.
- Shared training utilities live in `common/` (config loading, epoch-loop
  helpers, metrics, checkpointing, schedulers, early stopping, TensorBoard
  logging, seeding). Task code stays thin; shared logic is never duplicated.
- Training writes TensorBoard events to `logs/` and checkpoints to
  `checkpoints/`. Scripts turn those logs into CSVs and figures for the report.
- The graded exercises report is `reports/exercises.pdf` (LaTeX, committed);
  `docs/` posts accompany it on the site.

## Prerequisites

Everything runs **inside a Docker container**, so the host needs only:

- **Docker Engine** or Docker Desktop: [installation instructions](https://docs.docker.com/engine/install/)
- **Docker Compose** (included with Docker Desktop): [installation instructions](https://docs.docker.com/compose/install/)
- For GPU mode only: the **NVIDIA Container Toolkit**: [installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html). CPU mode needs no GPU.

No Python or Ruby toolchain is required on the host.

## Quickstart

```bash
git clone https://github.com/tronglh241/co5085_excersises_and_assignments
cd co5085_excersises_and_assignments

cp .env.example .env         # once; set ids from `id -u` / `id -g`
scripts/shell/dev.sh [gpu|cpu]   # default gpu (RUNS ON HOST)
```

All commands in the sections below run inside this container shell,
except `scripts/build_tex.sh` (report PDF), which orchestrates Docker from the host.

## Usage

### Train and evaluate

Pattern (per task; see the task `README.md` for its configs):

```bash
python E1/train.py --config E1/configs/softmax.yaml
python E1/evaluate.py --config E1/configs/softmax.yaml --checkpoint <run>/best.pt
```

TensorBoard events are written to `logs/` and checkpoints to `checkpoints/`.

### Inspect results

```bash
scripts/tensorboard.sh [logdir]                                 # live curves at localhost:6006 (default: logs/)
python scripts/extract_tensorboard.py [--logdir <run|parent>]   # per-run metrics.csv for plotting
```

`--logdir` is optional. It accepts a single run directory or a parent directory
containing several runs.

### Report PDF

```bash
scripts/shell/latex.sh   # open the latex container shell (RUNS ON HOST)
scripts/build_tex.sh [texfile]   # inside it: builds the PDF (default reports/exercises.tex)
```

### Docs site

```bash
scripts/serve.sh   # live preview at localhost:4000/co5085_excersises_and_assignments/
scripts/build.sh   # CI gate; run before every push
```

### Code style

```bash
scripts/lint.sh    # isort + flake8 over the Python packages
```

## Layout

```text
E1/ E2/ E3/ A1/ A2/            task dirs: README, configs, datasets, models,
                               train.py, evaluate.py, scripts/
common/                        our training utils (config, loop, metrics,
                               checkpoint, scheduler, early stopping, tb, seed)
reports/                       exercises.tex -> exercises.pdf (committed)
docs/                          Report site
dockers/                       Dockerfile (code+jekyll) + Dockerfile.latex (report PDF)
scripts/                       dev entry points + extract_tensorboard.py
data/ checkpoints/ logs/       runtime artifacts, gitignored: never commit
```
