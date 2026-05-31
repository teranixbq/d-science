---
title: "Data Representation: Tables & Images"
date: 2026-05-31
abstract: "A demonstration of how data tables and multimedia assets are rendered within the vintage editorial theme, utilizing Hugo render hooks."
categories: ["Documentation"]
tags: ["formatting", "demo"]
enablecomment: true
---

Information density is a hallmark of good data science reporting. We often need to represent datasets and visual graphs. Below is a demonstration of how tables and images look in this theme.

## 1. Markdown Table

Tables are rendered using standard Markdown syntax. The theme's CSS will automatically apply a ledger-like style to them, with uppercase headers and dashed borders.

| Algorithm | Complexity | Training Time | Accuracy (%) | Note |
| :--- | :--- | :--- | :--- | :--- |
| Random Forest | $O(v \cdot n \log n)$ | 45 mins | 89.4 | Baseline model |
| Support Vector Machine | $O(n^2)$ | 2.3 hrs | 91.2 | High variance |
| Multi-layer Perceptron | $O(n^3)$ | 6.5 hrs | 94.8 | Requires scaling |
| Transformer (DistilBERT) | $O(n^2 \cdot d)$ | 18 hrs | 98.1 | Resource intensive |

The table above is fully responsive and will scroll horizontally on smaller screens if necessary (though you may need to wrap it in a `div` if it gets extremely wide).

## 2. Lazy Loaded Image

Below is a standard Markdown image. Thanks to our custom Hugo Render Hook, the `loading="lazy"` and `decoding="async"` attributes are automatically injected into the HTML. 

The image is also styled with a vintage grayscale filter by default, which reveals its original color when hovered.

![A classic computer terminal showcasing data visualization.](https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1200&auto=format&fit=crop "Fig 1. Data visualization workstation. Hover to see colors.")

As you can see, inserting an image requires nothing more than the standard markdown `![Alt text](URL "Title")`. The "Title" attribute automatically becomes the caption below the image.

## Conclusion

By keeping the syntax standard, writers do not need to memorize complex HTML or shortcodes. The theme does all the heavy lifting in the background.
