import torch

from .base import Metric
from .confusion_matrix import ConfusionMatrix


def recall_from_cm(cm):
    cm = cm.float()
    row_sum = cm.sum(dim=1)
    return torch.where(row_sum > 0, cm.diag() / row_sum.clamp_min(1e-12), torch.zeros_like(row_sum))


class Recall(Metric):
    def __init__(self, num_classes):
        self.cm = ConfusionMatrix(num_classes)
        self.reset()

    def reset(self):
        self.cm.reset()

    def update(self, output):
        self.cm.update(output)

    def compute(self):
        return recall_from_cm(self.cm.compute())
