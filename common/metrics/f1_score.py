import torch

from .base import Metric
from .confusion_matrix import ConfusionMatrix
from .precision import precision_from_cm
from .recall import recall_from_cm


class F1Score(Metric):
    def __init__(self, num_classes):
        self.cm = ConfusionMatrix(num_classes)
        self.reset()

    def reset(self):
        self.cm.reset()

    def update(self, output):
        self.cm.update(output)

    def compute(self):
        precision = precision_from_cm(self.cm.compute())
        recall = recall_from_cm(self.cm.compute())
        denom = precision + recall
        return torch.where(denom > 0, 2 * precision * recall / denom.clamp_min(1e-12), torch.zeros_like(denom))
