---
title: "Image Segmentation: Semantic, Instance, and Panoptic"
date: 2026-07-15
author: "Teranix"
abstract: "A structured comparison of the three main paradigms in image segmentation — what each one solves, where each one is used, and how the field has converged toward unified architectures."
categories: ["Computer Vision", "Deep Learning"]
tags: ["segmentation", "semantic", "instance", "panoptic", "computer-vision"]
enablecomment: true
---

Image segmentation assigns meaning to every pixel in an image. The field has evolved from binary foreground/background separation to rich scene understanding that distinguishes individual object instances within a unified representation.

## 1. Three Paradigms

**Semantic segmentation** assigns a class label to every pixel, but does not distinguish between individual instances of the same class. All cars receive the label `car`, regardless of how many cars are present.

**Instance segmentation** detects individual object instances and produces a binary mask for each. It does not label background pixels.

**Panoptic segmentation** unifies both: every pixel receives both a class label and, for countable objects, an instance ID. It is the most complete representation.

{{< chart title="mIoU Progression on COCO (Semantic)" type="line" >}}
{
  "labels": ["2015", "2017", "2019", "2021", "2023"],
  "datasets": [{
    "label": "mIoU (%)",
    "data": [37, 51, 58, 65, 72]
  }]
}
{{< /chart >}}

## 2. Core Architectures

### Encoder-Decoder (U-Net)

U-Net is the dominant architecture for semantic segmentation. The encoder progressively downsamples the input to extract high-level features. The decoder upsamples back to the original resolution. Skip connections from encoder to decoder preserve spatial detail.

```python
import torch
import torch.nn as nn

class UNetBlock(nn.Module):
    """Basic U-Net double convolution block."""
    def __init__(self, in_channels, out_channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):
        return self.block(x)
```

### Mask R-CNN for Instance Segmentation

Mask R-CNN extends the Faster R-CNN object detector with a mask prediction head. For each detected bounding box, a small FCN predicts a binary mask. The key design choice is predicting masks per class in parallel rather than with competition across classes.

## 3. Evaluation Metrics

| Task | Primary Metric | Definition |
| :--- | :--- | :--- |
| Semantic | mIoU | Mean intersection over union across classes |
| Instance | AP | Average precision at multiple IoU thresholds |
| Panoptic | PQ | Panoptic quality = SQ × RQ |

Panoptic Quality (PQ) decomposes into Segmentation Quality (SQ, average IoU of matched segments) and Recognition Quality (RQ, F1 score of segment matching).

## 4. Modern Unified Approaches

Recent work has moved toward transformer-based architectures that handle all three segmentation tasks in a single model. Mask2Former treats all segmentation tasks as mask classification — the same architecture, trained on different supervision, achieves state-of-the-art on semantic, instance, and panoptic benchmarks simultaneously.

## 5. Conclusion

The convergence toward unified architectures reflects a maturing understanding: segmentation is fundamentally a mask classification problem regardless of task type. The practical implication is that teams building vision systems no longer need to maintain separate models for different segmentation paradigms.
