---
title: "Transfer Learning in Computer Vision: Fine-Tuning Pre-trained Models"
date: 2026-07-25
author: "Teranix"
abstract: "Transfer learning allows practitioners to leverage representations learned on large datasets and adapt them to new tasks with limited data. This note covers the mechanics of fine-tuning, layer freezing strategies, and practical considerations for common vision tasks."
categories: ["Computer Vision", "Deep Learning"]
tags: ["transfer-learning", "fine-tuning", "computer-vision", "deep-learning", "pytorch"]
enablecomment: true
---

Training a deep convolutional network from scratch requires millions of labeled examples and significant compute. Transfer learning sidesteps this by starting from a model pre-trained on a large dataset — typically ImageNet — and adapting it to a target task with far less data.

## 1. Why Transfer Learning Works

Pre-trained models encode a general visual hierarchy in their weights. Early layers detect low-level features: edges, corners, color gradients. Middle layers compose these into textures and parts. Later layers represent semantic concepts specific to the pre-training dataset.

When you fine-tune for a new task, the lower layers rarely need to change much — edges and textures are universal. The upper layers, which encode ImageNet-specific semantics, need to adapt to the new class distribution. This locality of required change is what makes transfer learning efficient.

## 2. Freezing Strategies

The key decision in fine-tuning is which layers to freeze (keep fixed) and which to train.

```python
import torchvision.models as models
import torch.nn as nn

# Load a ResNet-50 pre-trained on ImageNet
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

# Strategy 1: Freeze everything except the final classifier
for param in model.parameters():
    param.requires_grad = False

# Replace the classifier head for your target number of classes
num_classes = 10
model.fc = nn.Linear(model.fc.in_features, num_classes)
# Only model.fc parameters have requires_grad=True

# Strategy 2: Freeze only the early layers (layer1, layer2)
for name, param in model.named_parameters():
    if name.startswith(('layer1', 'layer2', 'conv1', 'bn1')):
        param.requires_grad = False
    else:
        param.requires_grad = True
```

The right strategy depends on dataset size and domain similarity:

| Dataset Size | Domain Similarity | Recommended Strategy |
|---|---|---|
| Small | Similar | Freeze all, train head only |
| Small | Different | Freeze early layers, fine-tune late layers |
| Large | Similar | Fine-tune entire network, low LR |
| Large | Different | Fine-tune entire network, normal LR |

## 3. Learning Rate Scheduling

Fine-tuning pre-trained weights requires careful learning rate selection. Too high and you destroy the pre-trained representations; too low and convergence is slow.

A common approach is differential learning rates — assigning lower learning rates to earlier layers and higher rates to the classification head:

```python
import torch.optim as optim

optimizer = optim.Adam([
    {'params': model.layer1.parameters(), 'lr': 1e-5},
    {'params': model.layer2.parameters(), 'lr': 1e-5},
    {'params': model.layer3.parameters(), 'lr': 1e-4},
    {'params': model.layer4.parameters(), 'lr': 1e-4},
    {'params': model.fc.parameters(),     'lr': 1e-3},
])
```

A cosine annealing scheduler on top of this decays learning rates smoothly over training, which often outperforms step decay for fine-tuning tasks.

## 4. Data Augmentation for Small Datasets

When the target dataset is small, aggressive augmentation is essential to prevent overfitting. Standard augmentations for vision fine-tuning:

```python
from torchvision import transforms

train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
    transforms.RandomRotation(15),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet statistics
        std=[0.229, 0.224, 0.225]
    )
])
```

Always normalize using the statistics of the pre-training dataset (ImageNet in this case), not your target dataset. The pre-trained weights expect inputs in that distribution.

## 5. Practical Results

Fine-tuning a ResNet-50 on a 1,000-image medical imaging dataset typically achieves 85–92% accuracy depending on domain. Training from scratch on the same dataset typically yields 60–70%. The gap narrows as dataset size grows, and by ~100k images, scratch training becomes competitive in similar domains.

For very small datasets (< 500 images), consider feature extraction without any fine-tuning: pass images through the frozen backbone, extract penultimate layer features, and train a simple linear classifier or SVM on those features. This avoids overfitting entirely.
