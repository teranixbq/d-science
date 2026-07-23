---
title: "Dense Retrieval with Bi-Encoders"
date: 2026-07-10
abstract: "How dense passage retrieval (DPR) and bi-encoder architectures revolutionized information retrieval by representing queries and documents as dense vectors in a shared embedding space."
categories: ["Information Retrieval"]
tags: ["retrieval", "dense-retrieval", "embeddings", "bi-encoder", "neural"]
enablecomment: true
---

Dense retrieval replaces sparse term-matching with continuous vector representations. Instead of counting term frequencies, a neural encoder maps both queries and documents into a shared embedding space where semantic similarity can be measured via dot product or cosine similarity.

## 1. Bi-Encoder Architecture

A bi-encoder uses two separate encoders (usually BERT-based) to independently encode the query and document.

```
Query  →  Encoder_Q  →  q_vec  ┐
                                 ├─ sim(q_vec, d_vec) → score
Doc    →  Encoder_D  →  d_vec  ┘
```

The key advantage: documents can be **pre-encoded offline** and stored in a vector index. Only the query needs to be encoded at query time.

## 2. Similarity Function

$$\text{score}(q, d) = E_Q(q)^T \cdot E_D(d)$$

Where `E_Q` and `E_D` are the query and document encoders respectively.

## 3. Building a Simple Dense Retrieval System

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class DenseRetriever:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.doc_embeddings = None
        self.documents = []
    
    def index(self, documents):
        """Pre-encode all documents offline."""
        self.documents = documents
        self.doc_embeddings = self.model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=True
        )
    
    def retrieve(self, query, top_k=5):
        """Encode query and find top-k most similar documents."""
        q_emb = self.model.encode(query, normalize_embeddings=True)
        scores = np.dot(self.doc_embeddings, q_emb)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        return [
            {'doc': self.documents[i], 'score': float(scores[i])}
            for i in top_indices
        ]

retriever = DenseRetriever()
retriever.index([
    "Dense retrieval uses neural embeddings",
    "BM25 is a sparse retrieval method",
    "Transformers changed NLP forever",
])

results = retriever.retrieve("neural search methods")
for r in results:
    print(f"{r['score']:.4f} | {r['doc']}")
```

## 4. Sparse vs Dense Comparison

| Aspect | Sparse (BM25) | Dense (Bi-Encoder) |
| :--- | :--- | :--- |
| Representation | Term frequency vectors | Dense float vectors |
| Semantic understanding | Weak (exact match) | Strong (semantic similarity) |
| Index size | Small | Large (embedding dimensions) |
| Query latency | Very fast | Faster with ANN index |
| Out-of-vocabulary | Fails | Handles via subword tokens |

## 5. Approximate Nearest Neighbor Search

With millions of documents, exact dot product search is too slow. Libraries like **FAISS** or **Annoy** provide approximate nearest neighbor (ANN) search with sub-linear time complexity.

## 6. Conclusion

Dense retrieval has become the foundation of modern RAG (Retrieval-Augmented Generation) pipelines. However, it works best when combined with sparse retrieval in a hybrid approach.
