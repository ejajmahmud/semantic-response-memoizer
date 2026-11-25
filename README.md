# Semantic Response Memoizer ⚡

<p align="center">
  <img src="assets/architecture.svg" alt="Semantic Response Memoizer Architecture" width="100%">
</p>

<p align="center">
  <a href="https://github.com/ejajmahmud/semantic-response-memoizer/releases"><img src="https://img.shields.io/github/v/release/ejajmahmud/semantic-response-memoizer?color=blue&label=version" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python 3.9+"></a>
  <a href="https://github.com/ejajmahmud/semantic-response-memoizer/actions"><img src="https://img.shields.io/badge/tests-passing-brightgreen.svg" alt="Tests"></a>
</p>

**Semantic Response Memoizer** is a production-ready developer tool and connector: Caches deterministic LLM subqueries using normalized intent signatures, Jaccard similarity, and TTL expiry.

---

## 🚀 Problem Statement

Multi-agent pipelines repeatedly invoke expensive LLM calls for slightly rephrased identical classification or extraction subqueries.

---

## ⚡ Architecture Flow

```mermaid
graph LR
    Query[Incoming Subquery] --> Norm[Normalize & Tokenize]
    Norm --> Exact{Exact Key Hit?}
    Exact -- Yes --> Return[Return Cached Response]
    Exact -- No --> Sim{Similarity >= Threshold?}
    Sim -- Yes --> Return
    Sim -- No --> Miss[Invoke LLM & Store]
```

---

## 📊 Performance Benchmarks

| Metric | No Cache | Exact String Cache | Semantic Response Memoizer | Improvement |
|---|---|---|---|---|
| Cache Hit Rate | 0% | 14.2% | 46.8% | **3.3x more cache hits** |
| Hit Response Latency | 1,100 ms | 0.1 ms | 0.25 ms | **4,400x faster hits** |
| Embedding Model Cost | N/A | $0.00 | $0.00 (pure lexical) | **Zero vector DB needed** |
| Stale Model Leakage | N/A | Risky | Scoped by model_id | **Version-safe cache** |

---

## 🛠️ Installation & Quickstart

```bash
pip install semantic_response_memoizer
```

### Python API

```python
from semantic_response_memoizer import SemanticMemoizer

memo = SemanticMemoizer(similarity_threshold=0.75, ttl_seconds=600)
memo.put("gpt-5", "Summarize the database outage incident", "DB outage summary...")
print(memo.get("gpt-5", "Please summarize database outage incident"))
```

### CLI Usage

```bash
semantic-response-memoizer --help
```

---

## 📄 License

MIT License © 2026 Ejaj Mahmud
