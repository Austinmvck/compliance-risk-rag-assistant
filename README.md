# Compliance Risk RAG Assistant

## Project Summary

The Compliance Risk RAG Assistant is a source-grounded AI workflow for third-party risk and compliance research.

The project is designed as an AI/data Product Management artifact. Its purpose is to demonstrate judgment around retrieval quality, source traceability, conflicting evidence, abstention, evidence sufficiency, and human-review controls.

This is not a production compliance system. It is a scoped prototype showing how a product manager might design and evaluate a source-grounded AI assistant for risk workflows.

## Start Here

For a quick review of the project, read these files in order:

1. [Architecture Diagram](Docs/architecture_diagram.md) — shows how evidence moves through the system, which retrieval path currently feeds Claude, where abstention occurs, and where semantic and hybrid retrieval fit as evaluated alternatives.
2. [Product Tradeoffs](Docs/product_tradeoffs.md) — explains why sparse retrieval remains the current generation default, why semantic retrieval and hybrid retrieval were evaluated but not defaulted, and why the project avoids overbuilding.
3. [System Walkthrough](Docs/system_walkthrough.md) — walks through what happens when a user asks a question, including evidence retrieval, thresholding, generation, abstention, and human review.
4. [Retrieval Evaluation Matrix](Docs/retrieval_evaluation_matrix_week_4.md) — documents retrieval behavior across direct evidence, conflicting evidence, missing evidence, and semantic threshold testing.
5. [Human Review Decision Table](Docs/human_review_decision_table.md) — defines when the system should route to analyst review instead of treating an answer as final.
6. [Hybrid Retrieval Notes](Docs/hybrid_retrieval_notes_week_5.md) — summarizes the hybrid Reciprocal Rank Fusion retrieval experiment and why it was tested but deferred as the default path.
7. [Week 4 Closeout](Docs/week_4_closeout.md) — summarizes the Week 4 evidence-control and retrieval-evaluation work.

## Current Workflow

The current generation workflow is:

```text
Source documents
→ metadata extraction
→ sentence-aware chunking
→ processed chunks
→ sparse retrieval
→ similarity thresholding
→ retrieved evidence package
→ Claude grounded answer or abstention
→ human-review guidance
```

The system uses synthetic third-party risk source documents covering corporate registry data, sanctions screening, cyber monitoring, and vendor questionnaire evidence.

Semantic retrieval and hybrid retrieval are implemented and evaluated, but they do not feed Claude by default.

## Current Retrieval Decision

The current generation path is:

```text
sparse retrieval → thresholding → Claude grounded answer
```

Semantic retrieval and hybrid retrieval are implemented and evaluated, but they do not feed Claude by default.

The current decision is:

```text
Sparse retrieval = current generation default
Semantic retrieval = evaluated alternative
Hybrid retrieval = tested with RRF and deferred
```

This decision is based on evidence behavior in the evaluation set. Sparse retrieval performed more safely on unsupported allegation handling, while semantic and hybrid retrieval introduced or preserved related-but-non-answering evidence failure modes.

## Implemented

Current implemented capabilities include:

- Synthetic third-party risk source corpus.
- Source metadata extraction, including source ID, source name, source date, source type, and entity.
- Sentence-aware chunking to preserve complete evidence claims and qualifiers.
- Sparse keyword retrieval baseline with query expansion.
- Minimum similarity thresholding to block low-relevance chunks.
- No-relevant-evidence behavior that prevents Claude from being called when retrieval returns no usable evidence.
- Semantic retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
- Semantic threshold testing across direct evidence, conflicting evidence, missing evidence, and unsupported allegation cases.
- Hybrid retrieval experiment using Reciprocal Rank Fusion.
- Sparse-vs-semantic-vs-hybrid retrieval evaluation across direct fact, sanctions ambiguity, cyber risk, conflicting evidence, and missing-evidence questions.
- Claude grounded answer generation using only retrieved evidence.
- Structured answer format with evidence used, source references, unknowns, confidence, and human-review guidance.
- Human-review decision table for sanctions ambiguity, unsupported allegations, conflicting cyber evidence, vendor self-report gaps, stale sources, and low retrieval confidence.
- Architecture diagram explaining current generation flow and evaluated retrieval alternatives.
- Product tradeoffs document explaining why sparse retrieval remains the default path.
- System walkthrough explaining runtime behavior for ownership, sanctions ambiguity, cyber patching conflict, and unsupported bribery/corruption questions.

## Intentionally Out of Scope

The project intentionally does not include:

- Production deployment.
- User interface.
- Authentication or multi-user access.
- Real customer or vendor data.
- Automated final compliance decisions.
- Replacement of human analysts.
- Enterprise monitoring, logging, or security controls.
- Automated citation verification.
- Production vector database.
- Model fine-tuning.
- Agentic workflow orchestration.

These were left out intentionally to keep the artifact focused on retrieval quality, evidence handling, evaluation, and product-control design.

## Key Evaluation Findings

### Sparse retrieval was useful as a transparent baseline

The sparse retrieval baseline was easy to inspect and debug. It performed well when user questions had strong term overlap with source text or when query expansion mapped user wording to source terminology.

It also performed better than semantic retrieval on some abstention and conflict cases, especially the unsupported bribery/corruption question and the cyber patching conflict question.

### Semantic retrieval improved meaning-based matching but introduced new risks

Semantic retrieval correctly retrieved expected sources for several direct evidence questions, including ownership, sanctions ambiguity, cyber risk, and missing sanctions identifiers.

However, semantic retrieval also introduced false-positive retrieval risk. For the unsupported bribery/corruption question, it returned compliance-adjacent chunks even though none supported the specific allegation.

This showed that semantic similarity is not the same as evidence sufficiency.

### Hybrid retrieval improved coverage but did not solve evidence sufficiency

Hybrid retrieval was tested using Reciprocal Rank Fusion because sparse retrieval scores and semantic embedding scores are not directly comparable.

Hybrid retrieval improved conflict coverage, especially for the patching question because it surfaced both the vendor questionnaire and the later cybersecurity monitoring report.

However, hybrid retrieval still returned related-but-non-answering chunks for the unsupported bribery/corruption question. Because it did not solve evidence sufficiency, it is documented as an evaluated alternative and deferred as the default generation path.

### Thresholding improved abstention behavior

The Week 3 system could pass zero-score chunks to Claude and rely on the model to abstain. In Week 4, a minimum similarity threshold was added so no-relevant-evidence cases are blocked before generation.

This changed abstention from a prompt-only behavior into a retrieval-layer product control.

### Human review is required for consequential risk decisions

The human-review decision table defines when the assistant should answer, abstain, or route to analyst review.

Examples include possible sanctions matches with missing identifiers, unsupported bribery/corruption allegations, conflicting vendor and cyber evidence, vendor self-reports without supporting evidence, and stale or low-confidence sources.

## What This Project Proves

This project demonstrates:

- Understanding of source-grounded AI workflow design.
- Metadata-preserving document processing.
- Evidence chunking tradeoffs.
- Sparse, semantic, and hybrid retrieval evaluation.
- Retrieval thresholding as a product reliability control.
- Abstention behavior for unsupported questions.
- Conflicting-evidence handling.
- Source traceability and evidence inspection.
- Human-in-the-loop workflow design for compliance/risk use cases.
- Practical evaluation thinking for AI/data product management.
- Product judgment around current-state versus evaluated-alternative system design.

## What This Project Does Not Prove

This project does not prove:

- Production-scale RAG performance.
- Real-world compliance decision automation.
- Enterprise security, privacy, monitoring, or governance readiness.
- Performance on large or messy real-world corpora.
- Automated citation verification.
- Human analyst replacement.
- Machine learning model development or fine-tuning.
- Production vector database architecture.
- That semantic retrieval is always better than sparse retrieval.
- That hybrid retrieval automatically solves evidence sufficiency.

The project is intentionally scoped as an AI/data PM proof artifact, not a production ML system.

## Repo Guide

Key scripts:

- `Scripts/03_build_chunks.py` — parses source documents and creates sentence-aware chunks.
- `Scripts/04_retrieve_chunks.py` — sparse keyword retrieval baseline with thresholding.
- `Scripts/05_rag_answer.py` — sends retrieved evidence to Claude and blocks generation when no relevant evidence is retrieved.
- `Scripts/06_semantic_retrieve_chunks.py` — semantic embedding retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
- `Scripts/07_hybrid_retrieve_chunks.py` — hybrid retrieval experiment using Reciprocal Rank Fusion.

Key data files:

- `Data/sources/` — synthetic source documents.
- `Data/processed_chunks.json` — processed source chunks with metadata.

Key documentation:

- `Docs/architecture_diagram.md` — current architecture and retrieval-method layout.
- `Docs/product_tradeoffs.md` — product and system design tradeoffs.
- `Docs/system_walkthrough.md` — end-to-end runtime walkthrough.
- `Docs/retrieval_plan_week_3.md` — retrieval experiment design.
- `Docs/retrieval_notes_week_3.md` — Week 3 retrieval notes.
- `Docs/week_4_lessons.md` — Week 4 evidence-control lessons.
- `Docs/retrieval_evaluation_matrix_week_4.md` — sparse vs semantic retrieval evaluation and threshold findings.
- `Docs/hybrid_retrieval_notes_week_5.md` — hybrid RRF retrieval experiment notes.
- `Docs/human_review_decision_table.md` — human-review routing rules.
- `Docs/week_4_closeout.md` — Week 4 closeout summary.

Key outputs:

- `Outputs/rag_test_01_direct_fact.md` — direct fact retrieval output.
- `Outputs/rag_test_02_conflicting_evidence.md` — conflicting evidence output.
- `Outputs/rag_test_03_missing_evidence.md` — missing evidence / abstention output.

## Current Limitations

Known limitations:

- The corpus is small and synthetic.
- Semantic retrieval is evaluated on a limited test set.
- Hybrid retrieval is implemented as an evaluated experiment, but it is not the default generation path.
- Source-type weighting is not implemented.
- Query-intent routing is not implemented.
- Citation references are not automatically verified.
- The current workflow is script-based, not a deployed product.
- Human-review routing is documented but not implemented as an application workflow.
- The assistant does not make final risk or compliance decisions.

## Next Improvements

Potential next improvements:

- Build a one-command demo script for core test cases.
- Expand the final demo/evaluation table with more answerable, partially answerable, and unanswerable questions.
- Add source-type weighting for sanctions, cyber, registry, vendor questionnaire, and adverse media-style sources.
- Add query-intent routing so different question types can prioritize different source types.
- Add reranking or evidence-sufficiency scoring to reduce related-but-non-answering retrieval.
- Add automated citation verification.
- Improve final interview talk track and portfolio presentation.
- Add final resume and LinkedIn positioning language.