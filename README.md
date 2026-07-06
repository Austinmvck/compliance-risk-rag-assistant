# Compliance Risk RAG Assistant

## Project Summary

The Compliance Risk RAG Assistant is a source-grounded AI workflow for third-party risk and compliance research.

The project is designed as an AI/data Product Management artifact. Its purpose is to demonstrate judgment around retrieval quality, source traceability, conflicting evidence, abstention, and human-review controls.

This is not a production compliance system. It is a scoped prototype showing how a product manager might design and evaluate a source-grounded AI assistant for risk workflows.

## Current Workflow

The current workflow is:

```text
Source documents
→ metadata parsing
→ sentence-aware chunking
→ processed chunks
→ sparse retrieval baseline
→ semantic retrieval comparison
→ similarity thresholding
→ retrieved evidence
→ Claude grounded answer
→ abstention or human review
→ evaluation notes
```

The system uses synthetic third-party risk source documents covering corporate registry data, sanctions screening, cyber monitoring, and vendor questionnaire evidence.

## Implemented

Current implemented capabilities include:

- Synthetic third-party risk source corpus.
- Source metadata parsing, including source ID, source name, source date, source type, and entity.
- Sentence-aware chunking to preserve complete evidence claims and qualifiers.
- Sparse keyword retrieval baseline with query expansion.
- Minimum similarity thresholding to block low-relevance chunks.
- No-relevant-evidence behavior that prevents Claude from being called when retrieval returns no usable evidence.
- Semantic retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
- Sparse-vs-semantic retrieval comparison across direct fact, sanctions ambiguity, cyber risk, conflicting evidence, and missing-evidence questions.
- Claude grounded answer generation using only retrieved evidence.
- Structured answer format with evidence used, source references, unknowns, confidence, and human-review guidance.
- Human-review decision table for sanctions ambiguity, unsupported allegations, conflicting cyber evidence, vendor self-report gaps, stale sources, and low retrieval confidence.

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
- Sparse retrieval and semantic retrieval comparison.
- Retrieval thresholding as a product reliability control.
- Abstention behavior for unsupported questions.
- Conflicting-evidence handling.
- Source traceability and evidence inspection.
- Human-in-the-loop workflow design for compliance/risk use cases.
- Practical evaluation thinking for AI/data product management.

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

The project is intentionally scoped as an AI/data PM proof artifact, not a production ML system.

## Repo Guide

Key files:

- `Scripts/03_build_chunks.py` — parses source documents and creates sentence-aware chunks.
- `Scripts/04_retrieve_chunks.py` — sparse keyword retrieval baseline with thresholding.
- `Scripts/05_rag_answer.py` — sends retrieved evidence to Claude and blocks generation when no relevant evidence is retrieved.
- `Scripts/06_semantic_retrieve_chunks.py` — semantic embedding retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
- `Data/sources/` — synthetic source documents.
- `Data/processed_chunks.json` — processed source chunks with metadata.
- `Docs/retrieval_plan_week_3.md` — retrieval experiment design.
- `Docs/retrieval_notes_week_3.md` — Week 3 retrieval notes.
- `Docs/week_4_lessons.md` — Week 4 evidence-control lessons.
- `Docs/retrieval_evaluation_matrix_week_4.md` — sparse vs semantic retrieval evaluation.
- `Docs/human_review_decision_table.md` — human-review routing rules.
- `Outputs/rag_test_01_direct_fact.md` — direct fact retrieval output.
- `Outputs/rag_test_02_conflicting_evidence.md` — conflicting evidence output.
- `Outputs/rag_test_03_missing_evidence.md` — missing evidence / abstention output.

## Retrieval Method Decision

The current generation path uses sparse retrieval as the default. This is intentional for the current prototype because sparse retrieval performed better on the evaluated abstention and conflict cases, especially the unsupported bribery/corruption question and the cyber patching conflict question.

Semantic retrieval is implemented as a parallel evaluated retrieval method. It improved meaning-based matching on several direct evidence questions, but it also introduced false-positive retrieval risk when related compliance evidence did not actually answer the question.

A semantic threshold sweep showed that raising the threshold to `0.40` filtered out unsupported bribery/corruption false positives, but also risked filtering out evidence needed for conflict detection. For that reason, semantic retrieval is not used as the default generation path yet.

Hybrid retrieval, source-type weighting, and query-intent routing are documented as next improvements rather than claimed as current functionality.

## Current Limitations

Known limitations:

- The corpus is small and synthetic.
- Semantic retrieval is evaluated on a limited test set.
- The system does not yet use hybrid retrieval.
- Source-type weighting is not implemented.
- Query intent routing is not implemented.
- Citation references are not automatically verified.
- The current workflow is script-based, not a deployed product.
- Human-review routing is documented but not implemented as an application workflow.
- The assistant does not make final risk or compliance decisions.

## Next Improvements

Potential next improvements:

- Add a simple hybrid retrieval experiment combining sparse and semantic retrieval.
- Add source-type weighting for sanctions, cyber, registry, vendor questionnaire, and adverse media-style sources.
- Build a one-command demo script for core test cases.
- Add architecture diagram and system walkthrough.
- Expand the evaluation matrix with more source types and test questions.
- Improve final interview talk track and portfolio presentation.