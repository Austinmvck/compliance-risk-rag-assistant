# Week 4 Closeout

## Week 4 Objective

Week 4 focused on improving the reliability and product judgment of the Compliance Risk RAG Assistant.

The goal was to move beyond basic retrieval and generation by adding evidence-quality controls, retrieval evaluation, semantic retrieval comparison, abstention behavior, and human-review decision rules.

## What Changed This Week

### 1. Evidence Quality Controls

The chunking process was improved from character-based chunking to sentence-aware chunking. This helps preserve complete claims, qualifiers, and source context.

A minimum similarity threshold was also added to sparse retrieval so low-relevance chunks are not passed to Claude.

### 2. Abstention Before Generation

The RAG answer script now blocks generation when no relevant evidence is retrieved.

This means unsupported questions are handled before Claude is called, instead of relying only on prompt instructions for abstention.

### 3. Semantic Retrieval Evaluation

A semantic retrieval script was added using `sentence-transformers/all-MiniLM-L6-v2`.

Semantic retrieval improved meaning-based matching for several direct evidence questions, including ownership, sanctions ambiguity, cyber risk, and missing sanctions identifiers.

However, semantic retrieval also introduced related-but-non-answering retrieval risk. In the bribery/corruption test case, semantic retrieval returned corporate registry and sanctions chunks even though those chunks did not support or contradict the allegation.

### 4. Semantic Threshold Sweep

A threshold sweep was tested at `0.10`, `0.20`, `0.30`, and `0.40`.

The sweep showed that lower thresholds improved recall but allowed related non-answering evidence. A higher `0.40` threshold filtered out the unsupported bribery/corruption false positives, but it also risked filtering out evidence needed for conflict detection.

This showed that semantic threshold tuning alone does not fully solve evidence sufficiency.

### 5. Query Expansion Confound

The sparse retrieval baseline performed well partly because hand-written query expansions mapped user wording to expected source terminology.

This made sparse retrieval useful and transparent for the controlled prototype, but it may not scale to broader real-world usage without broader synonym handling, query-intent routing, hybrid retrieval, reranking, or source-type-aware retrieval.

### 6. Human-Review Decision Table

A human-review decision table was added to define when the system should answer, abstain, or route to analyst review.

The table covers possible sanctions matches, unsupported allegations, conflicting cyber evidence, vendor self-reports without supporting evidence, stale sources, low retrieval confidence, and high-consequence decisions.

### 7. README Truth Update

The README was updated to reflect the current system honestly.

It now explains what is implemented, what is intentionally out of scope, what the project proves, what it does not prove, and which retrieval method is the current generation default.

## Retrieval Method Decision

The current generation path uses sparse retrieval as the default.

This is intentional for the current prototype because sparse retrieval performed better on the evaluated abstention and conflict cases, especially:

- unsupported bribery/corruption allegation
- cyber patching conflict

Semantic retrieval is implemented as a parallel evaluated retrieval method, not the default generation path.

Hybrid retrieval, source-type weighting, and query-intent routing are documented as future improvements unless implemented later.

## Key Product Lessons

### Retrieval quality matters before generation

A source-grounded AI assistant is only as reliable as the evidence it retrieves. Bad or weak retrieval can cause the model to answer from irrelevant context.

### Semantic similarity is not evidence sufficiency

A chunk can be semantically related to the entity or compliance domain while still failing to answer the actual question.

### Abstention should not rely only on prompts

The retrieval layer should help decide when there is not enough evidence to answer. Blocking generation before Claude is called is safer than asking the model to self-police unsupported questions.

### Human review needs explicit rules

“Human in the loop” is too vague. Risk workflows need clear trigger conditions, evidence signals, system behavior, human actions, and ownership.

### Product scope matters

This project intentionally avoids UI, deployment, production vector databases, real customer data, and final compliance automation. The goal is to prove product judgment around evidence handling, retrieval evaluation, and risk workflow design.

## What Is Still Missing

The project does not yet include:

- hybrid retrieval
- source-type weighting
- query intent routing
- one-command demo script
- architecture diagram
- system walkthrough
- final interview talk track
- production monitoring or deployment

## Week 5 Priorities

Week 5 should focus on making the system easier to understand and explain:

1. Architecture diagram
2. Product tradeoffs document
3. System walkthrough
4. Optional hybrid retrieval experiment only if time remains
5. README navigation polish

## Final Week 4 Summary

Week 4 turned the project from a basic RAG prototype into a more credible AI/data product artifact.

The system now includes evidence-quality controls, retrieval thresholding, semantic retrieval evaluation, abstention before generation, human-review routing rules, and an explicit retrieval-method decision.

The strongest lesson from Week 4 is that building AI for risk workflows is not just about retrieving documents and calling a model. The product must control evidence quality, evaluate retrieval behavior, handle unsupported and conflicting evidence, and define where human judgment is required.