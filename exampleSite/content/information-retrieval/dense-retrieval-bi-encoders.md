---
title: "Dense Retrieval with Bi-Encoders"
date: 2026-07-12
author: "Teranix"
abstract: "How bi-encoder architectures enable scalable semantic search by embedding queries and documents into a shared vector space — architecture, training, and tradeoffs versus sparse retrieval."
categories: ["Information Retrieval"]
tags: ["dense-retrieval", "bi-encoder", "semantic-search", "embeddings"]
enablecomment: true
---

Sparse retrieval methods like BM25 match on exact lexical overlap. Dense retrieval encodes both queries and documents into dense vector representations, then retrieves by nearest-neighbor search in embedding space. This enables semantic matching — finding relevant documents even when they share no words with the query.

## 1. Bi-Encoder Architecture

A bi-encoder uses two independent encoders — typically the same pretrained transformer — to encode queries and documents separately. The similarity score is the dot product or cosine similarity of the resulting embeddings.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode corpus documents at indexing time
corpus = [
    "Convolutional networks learn spatial features from images",
    "BM25 is a probabilistic ranking function for text retrieval",
    "Gradient descent minimizes the loss function iteratively",
]
doc_embeddings = model.encode(corpus, normalize_embeddings=True)

# Encode query at search time
query = "how do neural networks process visual data"
query_embedding = model.encode(query, normalize_embeddings=True)

# Compute cosine similarity (dot product after normalization)
scores = np.dot(doc_embeddings, query_embedding)
ranked = np.argsort(scores)[::-1]

for idx in ranked:
    print(f"Score: {scores[idx]:.4f} | {corpus[idx]}")
```

## 2. Training: Contrastive Learning

Bi-encoders are trained with a contrastive objective. For each query, a positive document (relevant) and one or more negative documents (irrelevant) are provided. The model learns to push the query embedding closer to the positive and further from the negatives.

Hard negative mining — selecting negatives that are difficult to distinguish from positives — is the most important factor in training a high-quality bi-encoder.

## 3. Scaling with Approximate Nearest Neighbor Search

Exact nearest-neighbor search over millions of documents is too slow for production. Approximate nearest neighbor (ANN) libraries like FAISS partition the embedding space into clusters or use graph-based indices to retrieve approximate top-k results in milliseconds.

```python
import faiss
import numpy as np

# Build a flat index (exact search) — swap for IVF or HNSW for scale
dim = 384  # embedding dimension
index = faiss.IndexFlatIP(dim)  # inner product (= cosine after normalization)

# Add document embeddings
doc_embeddings_np = doc_embeddings.astype(np.float32)
index.add(doc_embeddings_np)

# Search
query_np = query_embedding.reshape(1, -1).astype(np.float32)
distances, indices = index.search(query_np, k=3)
```

## 4. Dense vs Sparse Retrieval

| Property | BM25 | Bi-Encoder |
| :--- | :--- | :--- |
| Matching | Lexical | Semantic |
| Index size | Small (inverted index) | Large (dense vectors) |
| Query latency | Very fast | Fast (with ANN) |
| Out-of-vocabulary | Fails | Handles well |
| Domain specificity | Good | Requires domain fine-tuning |

In practice, **hybrid retrieval** — combining BM25 and dense scores — consistently outperforms either alone, especially on out-of-domain queries.

## 5. Conclusion

Bi-encoders are the workhorse of modern semantic search. Their key advantage over cross-encoders is efficiency: documents are encoded once at index time, and retrieval requires only a vector similarity computation. For re-ranking a small candidate set where latency is less critical, cross-encoders provide higher accuracy.
