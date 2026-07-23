---
title: "Introduction to Information Retrieval"
date: 2026-07-01
abstract: "A foundational overview of information retrieval systems, covering the core concepts of indexing, querying, and ranking that underpin modern search engines."
categories: ["Information Retrieval"]
tags: ["retrieval", "indexing", "search", "tf-idf"]
enablecomment: true
---

Information retrieval (IR) is the science of obtaining relevant information from a collection of resources in response to a query. It forms the backbone of modern search engines, recommendation systems, and digital libraries.

## 1. Core Components

An IR system consists of three fundamental components: a document collection, a query interface, and a ranking mechanism.

| Component | Role | Example |
| :--- | :--- | :--- |
| Document Collection | Stores indexed content | Web pages, PDFs, articles |
| Query Interface | Accepts user input | Search bar, API endpoint |
| Ranking Mechanism | Orders results by relevance | TF-IDF, BM25, neural models |

## 2. The Indexing Pipeline

Before a document can be retrieved, it must be processed through an indexing pipeline.

```python
import re
from collections import defaultdict

def build_inverted_index(documents):
    """
    Builds a simple inverted index from a list of documents.
    Each document is a dict with 'id' and 'text' fields.
    """
    index = defaultdict(list)
    
    for doc in documents:
        tokens = re.findall(r'\w+', doc['text'].lower())
        for token in set(tokens):  # unique tokens per doc
            index[token].append(doc['id'])
    
    return dict(index)

docs = [
    {'id': 1, 'text': 'information retrieval systems'},
    {'id': 2, 'text': 'retrieval augmented generation'},
    {'id': 3, 'text': 'neural information processing'},
]

index = build_inverted_index(docs)
print(index['retrieval'])  # [1, 2]
```

## 3. TF-IDF Scoring

The most classical relevance scoring function is TF-IDF (Term Frequency–Inverse Document Frequency).

$$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \log\frac{N}{df(t)}$$

Where:
- `TF(t, d)` = frequency of term `t` in document `d`
- `N` = total number of documents
- `df(t)` = number of documents containing term `t`

## 4. Conclusion

TF-IDF remains a strong baseline for many retrieval tasks despite its simplicity. Modern systems build upon this foundation with dense vector representations and learned ranking functions.
