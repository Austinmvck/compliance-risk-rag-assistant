# Architecture Diagram

## Purpose

This document explains the current architecture of the Compliance Risk RAG Assistant.

The goal is to show how evidence moves through the system, which retrieval path currently feeds Claude, where abstention occurs, and where semantic and hybrid retrieval fit as evaluated alternatives.

This diagram reflects the current prototype. It does not show production components that have not been implemented.

## Current Architecture

```mermaid
flowchart TD

    A[Source Documents] --> B[Metadata Parsing]
    B --> C[Sentence-Aware Chunking]
    C --> D[Data/processed_chunks.json]

    D --> E[Sparse Retrieval<br/>Scripts/04_retrieve_chunks.py]
    E --> F[Similarity Thresholding]
    F --> G{Relevant evidence<br/>above threshold?}

    G -- No --> H[Abstain Before Generation<br/>Claude Not Called]
    G -- Yes --> I[Retrieved Evidence Package]
    I --> J[Claude Grounded Answer<br/>Scripts/05_rag_answer.py]

    J --> K[Structured Answer]
    K --> L[Evidence Used]
    K --> M[Unknowns / Limitations]
    K --> N[Confidence / Caution]
    K --> O[Human-Review Guidance]

    O --> P{Human Review Trigger?}
    P -- Yes --> Q[Analyst Review<br/>Sanctions / Cyber / Vendor Risk / Compliance]
    P -- No --> R[User Reviews Grounded Answer]

    D --> S[Semantic Retrieval<br/>Scripts/06_semantic_retrieve_chunks.py]
    S --> T[Semantic Threshold Sweep]
    T --> U[Retrieval Evaluation Matrix]

    D --> V[Hybrid RRF Retrieval<br/>Scripts/07_hybrid_retrieve_chunks.py]
    V --> W[Hybrid Experiment Notes]
    W --> X[Tested and Deferred<br/>Not Default Generation Path]

    U --> Y[Retrieval Method Decision]
    X --> Y

    Y --> Z[Sparse Retrieval Remains<br/>Current Generation Default]