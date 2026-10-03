import torch.nn as nn


class SoftmaxClassifier(nn.Module):
    """Linear model on the flattened image.

    Args:
        in_channels: input channels.
        image_size: spatial size, assumed square.
        num_classes: output classes.
    """

    def __init__(self, in_channels=1, image_size=28, num_classes=10):
        super().__init__()
        self.net = nn.Sequential(
            nn.Flatten(1),
            nn.Linear(in_channels * image_size * image_size, num_classes),
        )

    def forward(self, x):
        return self.net(x)
