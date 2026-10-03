# AGENTS.md

## 1. Context

Coursework repo for **Deep Learning and its Applications in Computer Vision**
(CO5085, HK261). Contains exercises E1–E4, assignments A1–A2, and a Jekyll
(Chirpy 7.6) report site that publishes the results.

Stack: PyTorch, ignite, flame, Docker.

Language of code/docs: English.

> **All commands run inside the Docker container.**

## 2. Requirements

- **E1** Image classification on a small set (MNIST / Fashion-MNIST / CIFAR-10):
  (i) softmax on flattened input, (ii) MLP on flattened input, (iii) CNN.
  Compare accuracy, capacity, error cases.
- **E2** Multi-Head Self-Attention implemented from scratch and with PyTorch
  modules. Try several tokenizations (patch, pixel/row, CNN-stem, CLS + patches)
  on the same small set.
- **E3** LSTM and GRU on sequences (e.g. MNIST as pixel/row sequence). Compare
  with a feed-forward / CNN baseline.
- **E4** Generative models on a small MNIST-like set: VAE, GAN, Diffusion.
  Visualize samples and latent space; compare quality vs. compute.
- **A1** Self-chosen large image dataset. CNN vs Transformer under several
  regimes: from scratch vs pretrained; frozen, partially frozen, full finetune.
  A1.1 = dataset + protocol; A1.2 = final comparison.
- **A2** Self-chosen topic (detection, segmentation, ...). Working pipeline +
  analysis of one related paper (method, experiments, limitations).
  A2.1 = topic + paper + data; A2.2 = implementation + write-up.

## 3. Project structure

```text
configs/{e,a}N/{train,test}/<name>.yml   flame experiment configs
datasets/{e,a}N/        torch datasets
handlers/               our ignite handlers/schedulers (fixes on top of third_party)
models/{e,a}N/          torch modules
scripts/{e,a}N/         runnable helpers (EDA, figures)
scripts/            dev entry points: shell.sh, build.sh, serve.sh, lint.sh, tensorboard.sh, extract_tensorboard.sh
docs/               Chirpy site: _posts/, _tabs/, _data/, assets/
third_party/        flame, ignite (git submodules, read-only)
data/ checkpoints/ logs/   runtime artifacts, gitignored
```

## 4. Third-party libraries

- **ignite** (pytorch/ignite): training engine, metrics, handlers.
- **flame** (tronglh241/flame): config-driven train/eval templates on top of
  ignite (engine factory, metrics, checkpoint / early-stopping / TensorBoard handlers).
- Both are installed editable via `requirements.txt`.
- **Never edit `third_party/`.** Fix behavior through config or our own code.

## 5. Flame usage

```bash
flame run <config.yml>    # trains or evaluates, depending on the config
```

Config blocks: `data`, `model`, `optimizer`, `loss_fn`, `engine`, `evaluators`,
`metrics`, handlers (`lr_scheduler`, `early_stopping`, `checkpoint`, `logging`).

Template: `configs/e1/train/softmax.yml`. One config per model/mode
(e.g. `configs/e1/train/{softmax,mlp,cnn}.yml`).

## 6. Dev environment

```bash
cp .env.example .env         # once; set ids from `id -u` / `id -g`
scripts/shell.sh [gpu|cpu]   # default gpu; repo mounted at /workspace
```

## 7. Train and test

```bash
flame run configs/e1/train/softmax.yml   # train
flame run configs/e1/test/softmax.yml     # evaluate
```

- TensorBoard events go to `logs/`, checkpoints to `checkpoints/`.
- Inspect curves with TensorBoard pointed at `logs/`.

```bash
scripts/tensorboard.sh [logdir]                   # live curves at localhost:6006 (default logs/)
python scripts/extract_tensorboard.py --logdir <run|parent> [--tags t1,t2] [--filename metrics.csv]
# writes <run>/metrics.csv (tag,step,wall_time,value) for offline reading/plotting
```

## 8. Serve the docs locally

```bash
scripts/serve.sh   # livereload at localhost:4000/co5085_excersises_and_assignments/
scripts/build.sh   # CI-equivalent gate; run before every push
```

- `_config.yml` is not hot-reloaded: restart `serve.sh` after editing it.
- Site timezone is `Asia/Ho_Chi_Minh`.

## 9. Writing a new post

File: `docs/_posts/YYYY-MM-DD-slug.md`

```yaml
layout: post
title: "..."
author: trong # or thien, key in docs/_data/authors.yml, not a display name
date: YYYY-MM-DD HH:MM:SS +0700
toc: true
comments: false
image:
  path: samples.png
  alt: ...
media_subpath: /assets/{e, a}N/
```

- Generate figures with scripts (e.g. `python scripts/e1/eda.py`) into `docs/assets/{e,a}N/` (e.g `docs/assets/e1/`); reference by filename (resolved via `media_subpath`).
- `scripts/build.sh` must pass before push.

## 10. Adding a new experiment

1. Dataset in `datasets/{e,a}N/`, model in `models/{e,a}N/`.
2. Train + test configs in `configs/{e,a}N/{train,test}/`.
3. EDA/figure script in `scripts/{e,a}N/` writing to `docs/assets/{e,a}N/`.
4. Post in `docs/_posts/` (section 9).
5. Run the checks in section 11.

## 11. Code style and definition of done

```bash
scripts/lint.sh [dirs...]   # default: datasets/ handlers/ models/ scripts/
```

- isort `--check` + flake8 (`max-line-length = 120`, `third_party` excluded).
- Done = lint passes, and `build.sh` passes if `docs/` changed.
