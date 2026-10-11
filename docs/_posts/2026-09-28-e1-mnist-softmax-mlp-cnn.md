---
layout: post
title: "E1: Softmax vs MLP vs CNN"
author: trong
date: 2026-09-28 00:00:00 +0700
toc: true
comments: false
---

## Requirement

E1 per `exercise.pdf` §2 (due 02/11/2026): three image classifiers on the small
dataset — softmax on a flatten vector, MLP on a flatten vector, CNN — compared
on accuracy, params/capacity, loss–accuracy curves, and error cases.

## Dataset

`datasets/mnist.py` — stratified 50k/10k/10k train/val/test split (seed 42).
EDA notes (counts, geometry, samples, balance) are in the PDF.

## Models

- Softmax — `models/e1/softmax.py` (linear on flatten(784))
- MLP — `models/e1/mlp.py` (784 → 256 → 128 → 10)
- CNN — `models/e1/cnn.py` (conv blocks + FC head)

## Training

- Loop: `common/engine/trainer.py` (`train_step`: forward → loss → backward → step)
- Configs: `configs/e1/train_softmax.yml`, `configs/e1/train_softmax_aug.yml`
  (augmented variant), `configs/e1/test_softmax.yml` (evaluation)

## Reproduce

Environment: [SETUP.md](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/SETUP.md)
(Docker `gpu` service recommended).

```bash
python scripts/train.py configs/e1/train_softmax.yml
python scripts/train.py configs/e1/train_softmax_aug.yml
python scripts/evaluate.py configs/e1/test_softmax.yml --checkpoint <path>
```

Outputs: checkpoints under `checkpoints/e1/<model>/`, logs under `logs/e1/<model>/`.
Seed 42 reruns reproduce bit-identically. MLP/CNN run lines land with their configs.

Full results, curves, and error analysis: `reports/exercises.pdf` §E1.
