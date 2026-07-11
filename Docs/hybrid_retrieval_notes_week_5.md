# Week 5 Hybrid Retrieval Experiment

## Purpose

This experiment tested whether hybrid retrieval could improve the Compliance Risk RAG Assistant’s evidence retrieval behavior.

By the end of Week 4, the system had three important findings:

1. Sparse retrieval performed well on abstention and conflict cases, especially when query expansion mapped user language to source terminology.
2. Semantic retrieval improved meaning-based matching, but it also returned related-but-non-answering chunks for unsupported allegations.
3. Semantic threshold tuning showed a recall/precision tradeoff: higher thresholds improved abstention but risked filtering out evidence needed for conflict detection.

Hybrid retrieval was tested to see whether combining sparse and semantic retrieval could improve coverage without weakening abstention behavior.

## Method

The experiment used Reciprocal Rank Fusion, or RRF, to combine sparse and semantic retrieval results.

RRF was chosen instead of raw score averaging because sparse retrieval scores and semantic embedding scores are not directly comparable.

Sparse retrieval scores are based on keyword or term overlap. Semantic retrieval scores are based on embedding cosine similarity. Because those scores live on different scales, averaging them directly would be misleading.

RRF combines ranked outputs instead of raw scores.

```text
RRF score = 1 / (k + sparse_rank) + 1 / (k + semantic_rank)
```