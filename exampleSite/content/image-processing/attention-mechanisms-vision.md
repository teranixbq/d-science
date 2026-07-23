---
title: "Attention Mechanisms in Vision: From SENet to Vision Transformers"
date: 2026-07-22
author: "Teranix"
abstract: "Attention mechanisms allow vision models to focus computational resources on the most relevant parts of an image. This note traces the evolution from channel attention in SENet to the full self-attention of Vision Transformers."
categories: ["Computer Vision", "Deep Learning"]
tags: ["attention", "vision-transformer", "senet", "deep-learning", "computer-vision"]
enablecomment: true
---

Attention in deep learning is a mechanism that allows a model to weight different parts of its input differently depending on context. In computer vision, attention has evolved from lightweight channel-wise gates to the full self-attention that powers Vision Transformers (ViT).

## 1. Channel Attention: SENet

Squeeze-and-Excitation Networks (SENet, Hu et al. 2018) introduced the simplest practical form of attention in CNNs. The idea is to learn a per-channel scaling factor that recalibrates feature maps based on global context.

The SE block has two steps:

**Squeeze**: Global average pooling reduces each feature map to a single scalar, producing a channel descriptor of shape `(C,)`.

**Excitation**: Two fully connected layers with a bottleneck produce a vector of per-channel weights in `[0, 1]` via sigmoid activation. These weights are then multiplied back onto the original feature maps.

```python
import torch
import torch.nn as nn

class SEBlock(nn.Module):
    def __init__(self, channels: int, reduction: int = 16):
        super().__init__()
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, channels // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(channels // reduction, channels, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, c, _, _ = x.shape
        # Squeeze
        y = self.pool(x).view(b, c)
        # Excitation
        y = self.fc(y).view(b, c, 1, 1)
        return x * y.expand_as(x)
```

SENet won ILSVRC 2017 with only a 10% parameter overhead over the base network. The mechanism is general — it can be inserted into any CNN architecture.

## 2. Spatial Attention: CBAM

The Convolutional Block Attention Module (CBAM) extends SENet by adding spatial attention on top of channel attention. After channel recalibration, CBAM computes a 2D attention map over spatial positions using max-pooling and average-pooling features concatenated along the channel axis, then convolved with a 7×7 kernel.

This allows the model to simultaneously ask "which channels matter?" and "where in the image should I look?"

## 3. Self-Attention and Vision Transformers

Vision Transformers (Dosovitskiy et al. 2020) apply the transformer self-attention mechanism directly to image patches. An image of size `H × W` is divided into non-overlapping patches of size `P × P`, each linearly projected into a `D`-dimensional embedding. The resulting sequence of `N = HW/P²` patch tokens is processed by a standard transformer encoder.

Self-attention computes, for each patch, a weighted sum of all other patches:

```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(q, k, v):
    d_k = q.shape[-1]
    scores = torch.matmul(q, k.transpose(-2, -1)) / (d_k ** 0.5)
    weights = F.softmax(scores, dim=-1)
    return torch.matmul(weights, v), weights
```

The key property: every patch attends to every other patch in a single layer. CNNs require many layers to build up long-range dependencies through successive local receptive fields. ViT captures them immediately.

## 4. ViT vs CNN: Practical Tradeoffs

| Property | CNN | ViT |
|---|---|---|
| Inductive bias | Strong (locality, translation equivariance) | Weak |
| Data efficiency | High | Low (needs large datasets or pre-training) |
| Long-range dependencies | Via depth | Via self-attention in layer 1 |
| Compute scaling | Linear in image size | Quadratic in patch count |
| Transfer learning | Good | Excellent with large pre-training |

For most practical tasks with limited data, CNNs or hybrid models (ConvNeXt, EfficientNet) remain competitive. ViT shines when pre-trained on large corpora (ImageNet-21k, JFT) and fine-tuned downstream.

## 5. Efficient Attention for High-Resolution Images

The quadratic cost of self-attention becomes prohibitive at high resolution. Several approaches address this:

- **Swin Transformer**: Computes attention within local windows, shifting the windows between layers to allow cross-window communication
- **Focal Attention**: Attends to local tokens at fine granularity and global tokens at coarse granularity
- **Linear attention**: Approximates softmax attention with kernel methods, reducing complexity to O(N)

For most production vision systems in 2026, Swin-based architectures or ConvNeXt are the default choice — they combine the inductive biases of CNNs with the representational power of attention, without the data hunger of pure ViT.
