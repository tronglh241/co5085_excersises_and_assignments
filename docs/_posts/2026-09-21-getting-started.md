---
title: Getting Started
date: 2026-09-21
categories: [Guide]
tags: [setup]
pin: true
toc: true
---

## What this site is

Coursework reports for **CO5085 — Deep Learning and its Applications in
Computer Vision (HK261)**, by
[Le Huu Trong and Huynh Van Tam Thien]({% link _tabs/about.md %}#members).

## Exercises and assignments

**E1 — Classification (small set: MNIST / Fashion-MNIST / CIFAR-10).**
Softmax classifier and MLP on a flattened vector, plus a CNN classifier.
Compare accuracy, capacity, and error cases.

**E2 — Transformer / attention.**
Multi-Head Self-Attention implemented from scratch and with PyTorch modules.
Explore several tokenizations (patch, pixel/row, CNN-stem, CLS + patches, …)
and classify on the same small image set as E1.

**E3 — Sequence models.**
LSTM and GRU on sequential data (e.g. MNIST as a pixel/row sequence),
compared against a non-recurrent (MLP/CNN) baseline.

**E4 — Generative models.**
VAE, GAN, and Diffusion on a small image set (MNIST-like). Visualize samples
and latent space; discuss quality vs. compute.

**A1 — CNN vs Transformer at scale.**
Self-chosen large image dataset. Compare CNN vs Transformer under several
training regimes: from-scratch vs pretrained, and frozen / partially frozen /
fully fine-tuned backbones.
A1.1 = dataset + protocol. A1.2 = final comparison.

**A2 — Free topic.**
Self-chosen topic (detection, segmentation, …). Build a working pipeline and
analyze one related paper (method, experiments, limitations).
A2.1 = topic + paper + data. A2.2 = implementation + paper write-up.

## Setup

See [SETUP.md](https://github.com/tronglh241/co5085_excersises_and_assignments/blob/develop/SETUP.md)
in the repo for environment setup.
