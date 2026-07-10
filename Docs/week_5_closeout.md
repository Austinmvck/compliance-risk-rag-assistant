# Week 5 Closeout

## Purpose

This document summarizes Week 5 of the Compliance Risk RAG Assistant project.

Week 5 moved the project from retrieval experimentation into product packaging and system explanation. The goal was to make the prototype easier to understand, defend, and discuss in interviews.

This closeout summarizes what changed, what product decisions were confirmed, what artifacts were created, and what remains for Week 6.

## Week 5 Summary

The main Week 5 objective was to turn the source-grounded RAG prototype into a clearer AI/data Product Management artifact.

By the end of Week 5, the project had:

- a hybrid retrieval experiment using Reciprocal Rank Fusion
- an architecture diagram showing the current generation path and evaluated alternatives
- a product tradeoffs document explaining why certain decisions were made
- a system walkthrough showing what happens when a user asks a question
- an updated README that guides reviewers through the project
- a clearer distinction between current functionality, evaluated alternatives, and future improvements

The project is now more explainable and interview-ready.

## What Changed This Week

### 1. Hybrid retrieval was tested

Hybrid retrieval was implemented using Reciprocal Rank Fusion.

RRF was used because sparse retrieval scores and semantic embedding scores are not directly comparable. Instead of averaging raw scores, RRF combines ranked results.

The hybrid experiment showed that hybrid retrieval improved conflict coverage, especially for the cyber patching question. It surfaced both the vendor questionnaire and the later cybersecurity monitoring report.

However, hybrid retrieval still failed to solve evidence sufficiency. For the unsupported bribery/corruption question, it returned related-but-non-answering chunks that did not support the allegation.

### 2. Architecture was documented

The architecture diagram clarified how evidence moves through the system.

It showed:

- source documents
- metadata extraction
- sentence-aware chunking
- processed chunks
- sparse retrieval as the current generation path
- thresholding before generation
- Claude grounded answer generation
- abstention behavior
- human-review guidance
- semantic retrieval as an evaluated alternative
- hybrid retrieval as a tested and deferred alternative

The architecture doc made clear that semantic and hybrid retrieval do not feed Claude by default.

### 3. Product tradeoffs were documented

The product tradeoffs document explained why sparse retrieval remains the default generation path.

The key tradeoff was choosing the safest evidence path over the most advanced-sounding architecture.

Semantic retrieval improved meaning-based matching, and hybrid retrieval improved conflict coverage, but neither solved evidence sufficiency. Because of that, they were documented as evaluated alternatives rather than default generation paths.

### 4. Runtime behavior was explained

The system walkthrough documented what happens when a user asks a question.

It covered:

- ownership lookup
- sanctions ambiguity
- cyber patching conflict
- unsupported bribery/corruption allegation

The walkthrough clarified that Claude receives only the retrieved evidence package, not the full source corpus.

It also clarified that missing evidence should lead to abstention and that conflicting or high-consequence evidence should route to human review.

### 5. README navigation was updated

The README was updated to serve as the front door to the project.

It now guides reviewers through:

- architecture
- product tradeoffs
- system walkthrough
- retrieval evaluation
- human-review decision table
- hybrid retrieval notes
- Week 4 closeout

The README now better reflects the current Week 5 state of the project.

## Artifacts Created

Week 5 created or updated the following files:

- `Scripts/07_hybrid_retrieve_chunks.py`
- `Docs/hybrid_retrieval_notes_week_5.md`
- `Docs/architecture_diagram.md`
- `Docs/product_tradeoffs.md`
- `Docs/system_walkthrough.md`
- `README.md`

## Retrieval Decision Confirmed

The current generation path remains:

```text
sparse retrieval → thresholding → Claude grounded answer