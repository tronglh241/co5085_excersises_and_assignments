---
layout: post
title: "E1: Softmax vs MLP vs CNN"
author: trong
toc: true
comments: false
---

> **Requirement**: build and compare three classifiers on a small image set (MNIST) with a handwritten training loop. The classifiers are softmax and MLP on flattened inputs, and a CNN. The comparison covers accuracy, parameter count, loss and accuracy curves, and error cases.

## Code

| Type | Description | File |
|---|---|---|
| Model | Softmax | [`models/e1/softmax.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/models/e1/softmax.py) |
| Model | MLP | [`models/e1/mlp.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/models/e1/mlp.py) |
| Model | CNN | [`models/e1/cnn.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/models/e1/cnn.py) |
| Dataset | MNIST | [`datasets/mnist.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/datasets/mnist.py) |
| Training loop | Trainer | [`common/engine/trainer.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/common/engine/trainer.py) |
| Entry point | Training | [`scripts/train.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/scripts/train.py) |
| Entry point | Evaluation | [`scripts/evaluate.py`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/scripts/evaluate.py) |
| Config | Softmax training | [`configs/e1/train_softmax.yml`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/configs/e1/train_softmax.yml) |
| Config | Softmax training with augmentation | [`configs/e1/train_softmax_aug.yml`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/configs/e1/train_softmax_aug.yml) |
| Config | Softmax evaluation | [`configs/e1/test_softmax.yml`](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/configs/e1/test_softmax.yml) |

## Run

Set up the environment with [SETUP.md](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/co5085/SETUP.md).

### Train

```bash
python scripts/train.py configs/e1/train_softmax.yml
python scripts/train.py configs/e1/train_softmax_aug.yml
```

### Evaluate

```bash
python scripts/evaluate.py configs/e1/test_softmax.yml
```

To evaluate a different checkpoint, set the `loader.path` field in the config file.

## Results

Setup, tables, curves, and error analysis: *reports/exercises.pdf (upcoming)* §E1.
