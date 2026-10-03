---
layout: post
title: "E1: Softmax vs MLP vs CNN"
author: trong
date: 2026-09-28 00:00:00 +0700
toc: true
comments: false
image:
  path: samples.png
  alt: MNIST sample grid per digit
media_subpath: /assets/e1/
---

## 1. Introduction

*Purpose: problem statement (small-set image classification), chosen dataset, the three models in scope, and the three comparison axes — accuracy, capacity, error cases. End with a one-line roadmap and, later, the key takeaway.*

## 2. Dataset

### 2.1 Overview

*Purpose: dataset source and pool sizes, 28x28 grayscale geometry, 10 classes, stratified 50k/10k/10k split (seed 42); point to `datasets/e1/mnist.py`.*

### 2.2 EDA

*Purpose: figures + observations from `scripts/e1/eda.py` — counts, split share, sample grid, class balance.*

![Original counts](original_counts.png){: w="890" h="540" }
![Split counts](split_counts.png){: w="900" h="550" }
![Split share](split_share.png){: w="427" h="494" }
![Samples per digit](samples.png){: w="800" h="1000" }
![Class balance](class_balance.png){: w="890" h="544" }

*TBD: one-line observation per figure (split ratio, geometry, balance ratio, normalization stats).*

### 2.3 Preprocessing

*Purpose: normalization stats measured on train (mean/std) and why; link the transform config.*

## 3. Models

*Shared template per model below: intuition / inductive bias → architecture → #params → code reference.*

### 3.1 Softmax Classifier

*Purpose: linear baseline on flatten(784); no hidden layer, no spatial bias. Ref `models/e1/softmax.py`.*

### 3.2 MLP Classifier

*Purpose: dense 784 → 256 → 128 → 10 with ReLU (+dropout); still no spatial bias. Ref `models/e1/mlp.py`.*

### 3.3 CNN Classifier

*Purpose: [conv3x3/ReLU/MaxPool]x2 (16,32) + FC128 head; local receptive fields + pooling. Ref `models/e1/cnn.py`.*

### 3.4 Summary

*Purpose: design-time comparison table bridging into capacity. Param counts are deterministic from the model definitions.*

| Model | #Params | #FLOPS |
|---|---|---|---|
| Softmax | TBD | xxx |
| MLP | TBD | xxx |
| CNN | TBD | xxx |

## 4. Training Setup

*Purpose: everything shared across the three runs (from `configs/e1/train/*.yml`); per-model deviations noted inline.*

### 4.1 Loss

*Purpose: `CrossEntropyLoss` on logits; why; no class weighting (balanced set).*

### 4.2 Optimizer & Schedule

*Purpose: SGD lr=0.01 / momentum=0.9, batch 64 train / 512 eval, `ReduceLROnPlateau`, max epochs.*

### 4.3 Regularization & Augmentation

*Purpose: `RandomAffine(10°, translate 0.1)`, dropout / weight decay if any; per-model differences (currently TBD for MLP/CNN).*

### 4.4 Model Selection & Metrics

*Purpose: best checkpoint on val loss, early stopping, ignite metrics (accuracy/precision), test-set protocol.*

### 4.5 Reproducibility

*Purpose: seed, device, config paths, exact train commands, checkpoint/log locations.*

```bash
# TBD: exact commands used for the final runs
```

## 5. Results

### 5.1 Accuracy

*Purpose: TBD metrics table (train/val/test acc + loss, precision) + `train_curves.png`; interpretation of gaps.*

| Model | Train acc / loss | Val acc / loss | Test acc | Test precision |
|---|---|---|---|---|
| Softmax | TBD / TBD | TBD / TBD | TBD | TBD |
| MLP | TBD / TBD | TBD / TBD | TBD | TBD |
| CNN | TBD / TBD | TBD / TBD | TBD | TBD |

![Train/val curves](train_curves.png){: w="889" h="540" }

### 5.2 Capacity

*Purpose: TBD cost table (params, FLOPs, checkpoint size, sec/epoch) + train–val gap reading (under/overfit).*

| Model | #Params | FLOPs | Checkpoint | Sec/epoch |
|---|---|---|---|---|
| Softmax | TBD | TBD | TBD | TBD |
| MLP | TBD | TBD | TBD | TBD |
| CNN | TBD | TBD | TBD | TBD |

### 5.3 Error Cases

*Purpose: TBD confusion matrices + misclassified grid + error-taxonomy table with qualitative explanation.*

![Confusion (softmax)](confusion_softmax.png){: w="889" h="540" }
![Confusion (MLP)](confusion_mlp.png){: w="889" h="540" }
![Confusion (CNN)](confusion_cnn.png){: w="889" h="540" }
![Misclassified examples](errors_grid.png){: w="889" h="540" }

| Error type | Softmax | MLP | CNN |
|---|---|---|---|
| Shift/rotation sensitivity | TBD | TBD | TBD |
| Similar-shape digits | TBD | TBD | TBD |
| Thin/broken strokes | TBD | TBD | TBD |

### 5.4 Comparison Summary

*Purpose: TBD one-row-per-model table directly answering accuracy × capacity × errors — the graded ask.*

| Model | Accuracy | Capacity / cost | Main error mode |
|---|---|---|---|
| Softmax | TBD | TBD | TBD |
| MLP | TBD | TBD | TBD |
| CNN | TBD | TBD | TBD |

## 6. Conclusion

*Purpose: takeaways per axis, limitations, future work.*
