---
title: "Reranking with Cross-Encoders"
date: 2026-07-18
author: "Teranix"
abstract: "Cross-encoders score query-document pairs jointly, producing highly accurate relevance estimates at the cost of speed — making them ideal as a second-stage reranker on top of a fast first-stage retriever."
categories: ["Information Retrieval"]
tags: ["reranking", "cross-encoder", "bert", "retrieval"]
enablecomment: true
---

Modern retrieval pipelines rarely rely on a single model. The dominant pattern is a two-stage architecture: a fast first-stage retriever (BM25 or a bi-encoder) returns a candidate set of hundreds of documents, then a slower but more accurate second-stage reranker scores and reorders that set. Cross-encoders are the standard choice for the second stage.

## 1. Bi-Encoders vs Cross-Encoders

A bi-encoder encodes the query and document independently into dense vectors, then computes similarity via dot product. This is fast — documents can be indexed offline — but the query and document never interact during encoding, which limits accuracy.

A cross-encoder takes the concatenated query and document as a single input and produces a scalar relevance score. The full self-attention mechanism in a transformer allows every query token to attend to every document token, capturing fine-grained interactions that bi-encoders miss.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("cross-encoder/ms-marco-MiniLM-L-6-v2")
model = AutoModelForSequenceClassification.from_pretrained(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)
model.eval()

def score(query: str, document: str) -> float:
    inputs = tokenizer(
        query, document,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )
    with torch.no_grad():
        logits = model(**inputs).logits
    return logits.squeeze().item()

q = "what is the boiling point of water"
d = "Water boils at 100 degrees Celsius at standard atmospheric pressure."
print(f"Score: {score(q, d):.4f}")
```

## 2. Why Not Use Cross-Encoders for First-Stage Retrieval

The fundamental constraint is latency. Scoring a query against a corpus of one million documents with a cross-encoder requires one million forward passes — this is computationally prohibitive at query time.

| Stage | Model | Candidates In | Candidates Out | Latency |
|---|---|---|---|---|
| First stage | BM25 / bi-encoder | Full corpus (1M+) | 100–1000 | < 50ms |
| Second stage | Cross-encoder | 100–1000 | 10–50 | 100–500ms |

The reranker only sees a small candidate set, so latency remains acceptable.

## 3. Training Cross-Encoders

Cross-encoders are typically fine-tuned on query-document pairs with binary or graded relevance labels. The MS MARCO passage ranking dataset is the standard benchmark, containing ~500k queries with sparse relevance judgments from Bing query logs.

The training objective is binary cross-entropy over positive and negative pairs:

```python
import torch.nn as nn

criterion = nn.BCEWithLogitsLoss()

# positive pair: label = 1.0
# negative pair: label = 0.0
loss = criterion(scores, labels)
```

Hard negative mining — selecting negatives that the first-stage retriever ranks highly but are not relevant — significantly improves reranker quality compared to random negatives.

## 4. Listwise vs Pointwise Reranking

The approach above is pointwise: each document is scored independently. Listwise rerankers take the entire candidate list as input and produce a ranked permutation directly. Models like RankT5 and RankGPT follow this approach, though they require more compute per query.

## 5. Practical Tradeoffs

Cross-encoder reranking consistently improves NDCG@10 by 5–15% over a bi-encoder alone on standard benchmarks. The gains are largest when:

- The first-stage retriever has high recall but imprecise ranking
- Queries are ambiguous and require reading document context to resolve
- The domain is specialized (legal, medical, code) where lexical overlap is sparse

The cost is latency and infrastructure complexity. For latency-sensitive applications, distilled cross-encoders (6-layer MiniLM variants) offer a good tradeoff, running roughly 4× faster than full BERT-base with modest accuracy loss.
