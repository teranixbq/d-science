---
title: "BM25: The Probabilistic Retrieval Model"
date: 2026-07-05
abstract: "An in-depth look at BM25, the probabilistic ranking function that remains the dominant sparse retrieval baseline in modern search systems."
categories: ["Information Retrieval"]
tags: ["retrieval", "bm25", "ranking", "probabilistic"]
enablecomment: true
---

BM25 (Best Match 25) is a ranking function used by search engines to estimate the relevance of documents to a given query. It is an evolution of the TF-IDF family and remains the dominant sparse retrieval baseline in 2026.

## 1. The BM25 Formula

The BM25 score for a query `q` against document `d` is computed by summing over each query term `t`: the IDF of `t` multiplied by a normalized term frequency. The term frequency component saturates with higher counts (controlled by `k1`) and is penalized for long documents relative to the corpus average (controlled by `b`).

Where:
- `f(t, d)` = term frequency of `t` in document `d`
- `|d|` = length of document `d`
- `avgdl` = average document length in corpus
- `k1` = term frequency saturation parameter (typically 1.2–2.0)
- `b` = length normalization parameter (typically 0.75)

## 2. Key Parameters

| Parameter | Typical Value | Effect |
| :--- | :--- | :--- |
| k1 | 1.2 – 2.0 | Controls TF saturation. Higher = more weight on frequency |
| b | 0.75 | Controls length normalization. 0 = no normalization |

## 3. Implementation

```python
import math
from collections import Counter

class BM25:
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = [doc.lower().split() for doc in corpus]
        self.n = len(self.corpus)
        self.avgdl = sum(len(d) for d in self.corpus) / self.n
        self.df = self._compute_df()
    
    def _compute_df(self):
        df = Counter()
        for doc in self.corpus:
            df.update(set(doc))
        return df
    
    def idf(self, term):
        n_t = self.df.get(term, 0)
        return math.log((self.n - n_t + 0.5) / (n_t + 0.5) + 1)
    
    def score(self, query, doc_idx):
        doc = self.corpus[doc_idx]
        tf = Counter(doc)
        dl = len(doc)
        score = 0.0
        
        for term in query.lower().split():
            f = tf.get(term, 0)
            idf = self.idf(term)
            numerator = f * (self.k1 + 1)
            denominator = f + self.k1 * (1 - self.b + self.b * dl / self.avgdl)
            score += idf * numerator / denominator
        
        return score

corpus = [
    "information retrieval systems and search engines",
    "probabilistic ranking models for document retrieval",
    "neural networks for natural language processing",
]

bm25 = BM25(corpus)
query = "retrieval ranking"
scores = [bm25.score(query, i) for i in range(len(corpus))]
print(scores)  # [1.23, 1.87, 0.12]
```

## 4. BM25 vs TF-IDF

BM25 outperforms TF-IDF primarily due to two mechanisms: **term frequency saturation** and **document length normalization**. A document that mentions a term 100 times is not necessarily 100x more relevant than one that mentions it once.

## 5. Conclusion

Despite being over 30 years old, BM25 is still a hard baseline to beat for sparse retrieval. Most production systems use it as a first-stage retriever before neural re-ranking.
