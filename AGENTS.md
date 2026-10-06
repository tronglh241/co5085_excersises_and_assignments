# AGENTS.md

## 1. Context

Coursework repo for **Deep Learning and its Applications in Computer Vision**
(CO5085, HK261). Contains exercises E1–E3, assignments A1–A2, and a Jekyll
(Chirpy 7.6) report site that publishes the results.

Stack: PyTorch, ignite, flame, Docker.

Language of code/docs: English.

> **All commands run inside the Docker container.**

## 2. Requirements

- **E1** (due 02/11 W9): softmax / MLP / CNN classifiers on one small set
  (MNIST / Fashion-MNIST / CIFAR-10). Compare accuracy, params/capacity,
  loss–accuracy curves, error cases. No attention, RNN, regression, or generative
  models (in-class only, not graded).
- **E2** (due 02/11 W9): MSA from scratch (only `Linear`/`einsum`/`softmax` — no
  `nn.MultiheadAttention` for that version) plus a PyTorch-MSA counterpart;
  ≥2 tokenizations (patch, pixel/row, CNN-stem); same dataset as E1.
- **E3** (due 09/11 W10): LSTM **and** GRU (`nn.LSTM`/`nn.GRU` allowed) on ≥1
  sequence views of the same images (+ LSTM-vs-GRU comparison), vs the E1
  MLP/CNN baseline (checkpoint reuse or retrain on the same split).
- **A1** (A1.1 26/10: dataset + protocol; A1.2 09/11: full comparison):
  self-chosen LARGE set (not MNIST/Fashion-MNIST/CIFAR-10); ≥1 CNN and ≥1
  Transformer; from-scratch vs pretrained × freeze-backbone / freeze-partial /
  full-finetune. Pretrained weights from timm/torchvision/HF allowed.
- **A2** (A2.1 02/11: topic + paper + data; A2.2 16/11: implementation + write-up):
  self-chosen non-classification topic (segmentation, detection, ReID,
  generation, ...) with a working pipeline (≥2 methods/variants compared) plus
  a mandatory paper analysis (method, experiments, limitations).
- Submission: source in `E1/`, `E2/`, `E3/` (+ per-task README); **one common
  PDF** `reports/exercises.pdf` for all of E1–E3 (W9: E1+E2, W10: +E3);
  GitHub Pages links the repo and the PDF (page frame due 19/10 W7).

## 3. Project structure

```text
E1/ E2/ E3/ A1/ A2/   task dirs: README.md, configs/*.yaml, datasets/, models/,
                      train.py, evaluate.py, scripts/
common/               our training utils: config (vendored liberyacs), loop,
                      metrics, checkpoint, scheduler, early_stopping, tb, seed
reports/              exercises.tex -> exercises.pdf (committed)
docs/                 Chirpy site: _posts/, _tabs/, _data/, assets/
scripts/              dev entry points: shell/dev.sh, build.sh, serve.sh, lint.sh,
                      tensorboard.sh, shell/latex.sh, build_tex.sh + extract_tensorboard.py
dockers/              Dockerfile (code+jekyll) + Dockerfile.latex (report PDF)
data/ checkpoints/ logs/   runtime artifacts, gitignored
```

## 4. Dependencies (`requirements.txt`)

torch/torchvision (cu126 index), timm (A1 pretrained), yacs + pyyaml (config),
tensorboard, matplotlib, scikit-learn; flake8/isort for lint.
`common/config.py` is vendored from liberyacs (our own code):
`CfgNode.load(path)` evaluates `{module, name, kwargs}` blocks into objects and
string expressions against the config namespace (+ `extralibs` imports).

## 5. Training: our own loop (required by spec)

- Each task's `train.py` owns a **visible epoch loop**: forward → loss →
  backward() → optimizer.step(). `common.loop` provides only granular
  `train_epoch`/`evaluate` helpers — no `trainer.fit()`-style black box.
- Configs hold plain hyperparams plus `{module, name, kwargs}` object specs
  evaluated by `common.config.CfgNode`. One config per model/mode.
- Checkpoints are plain `torch.save` dicts
  (model/optimizer/scheduler/epoch/best/rng). Torch schedulers pickle natively.
- Metrics in `common.metrics`: accuracy, confusion matrix, per-class P/R.

## 6. Dev environment

```bash
cp .env.example .env         # once; set ids from `id -u` / `id -g`
docker compose build        # pulls torch/cu126, timm, TeX Live; slow first time
scripts/shell/dev.sh [gpu|cpu]   # default gpu; repo mounted at /workspace (RUNS ON HOST)
```

## 7. Train, evaluate, inspect

```bash
python E1/train.py --config E1/configs/softmax.yaml
python E1/evaluate.py --config E1/configs/softmax.yaml --checkpoint <run>/best.pt
scripts/tensorboard.sh [logdir]                   # live curves at localhost:6006 (default logs/)
python scripts/extract_tensorboard.py --logdir <run|parent> [--tags t1,t2] [--filename metrics.csv]
# writes <run>/metrics.csv (tag,step,wall_time,value) for offline reading/plotting
```

- TensorBoard events go to `logs/<task>/…`, checkpoints to `checkpoints/<task>/…`.
- Keep seed, config dump, and logs per run for reproducibility.

## 8. Reports (LaTeX, committed PDF)

- `reports/exercises.tex`: shared intro (dataset/split, common to E1–E3) plus one
  chapter per exercise (architecture, training, tables, learning curves, short
  remarks — not just accuracy lists).
- Report PDF builds in its own image (`dockers/Dockerfile.latex`,
  `texlive/texlive:latest-medium`); open it with `scripts/shell/latex.sh`,
  then run `scripts/build_tex.sh [texfile]` inside (default
  `reports/exercises.tex`). Commit `reports/exercises.pdf` (Pages links it).
- Posts under `docs/_posts/` stay as companions; link the PDF.

## 9. Serve the docs locally

```bash
scripts/serve.sh   # livereload at localhost:4000/co5085_excersises_and_assignments/
scripts/build.sh   # CI-equivalent gate; run before every push
```

- `_config.yml` is not hot-reloaded: restart `serve.sh` after editing it.
- Site timezone is `Asia/Ho_Chi_Minh`.

## 10. Writing a new post

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
media_subpath: /assets/{e,a}N/
```

- Generate figures with task scripts (e.g. `python E1/scripts/eda.py`) into
  `docs/assets/{e,a}N/`; reference by filename (resolved via `media_subpath`).
- `scripts/build.sh` must pass before push.

## 11. Adding a new experiment

1. Task dir `E*/`/`A*/`: `datasets/`, `models/`, `configs/*.yaml`, `train.py`,
   `evaluate.py`, per-task `README.md` (brief + run commands).
2. Shared logic goes in `common/`, never duplicated per task.
3. Figures via task `scripts/` into `docs/assets/`; chapter into `reports/`.
4. Run the checks in section 12.

## 12. Code style and definition of done

```bash
scripts/lint.sh [dirs...]   # default: datasets/ models/ scripts/ (+ common/, E*/ as they land)
```

- isort `--check` + flake8 (`max-line-length = 120`).
- Done = lint passes, and `build.sh` passes if `docs/` changed.

## 13. Git hygiene

Never commit `data/` `checkpoints/` `logs/` `.env` `docs/_site/`
`docs/.jekyll-cache/` (all ignored). Do commit `reports/exercises.pdf`.
Stage only intended files; inspect `git status`/`git diff` before committing.
