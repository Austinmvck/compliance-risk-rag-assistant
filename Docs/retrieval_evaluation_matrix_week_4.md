# Week 4 Retrieval Evaluation Matrix

## Purpose

This evaluation compares sparse keyword retrieval against semantic embedding retrieval for the Compliance Risk RAG Assistant.

The goal is not to prove that one retrieval method is always better. The goal is to understand which method retrieves better evidence for different compliance/risk question types.

## Retrieval Methods Compared

### Sparse retrieval baseline

Script: `Scripts/04_retrieve_chunks.py`

Characteristics:
- Uses token overlap, query expansion, and cosine similarity.
- Easier to inspect and debug.
- Performs well when query terms overlap with source terms or query expansion is targeted.
- Can miss relevant evidence when user wording differs from source wording.

### Semantic retrieval

Script: `Scripts/06_semantic_retrieve_chunks.py`

Characteristics:
- Uses `sentence-transformers/all-MiniLM-L6-v2`.
- Converts questions and chunks into embeddings.
- Ranks chunks by semantic similarity.
- Can retrieve evidence based on meaning rather than exact word overlap.
- Can also retrieve topically adjacent but unsupported evidence.

## Evaluation Table

| Test ID | Question | Expected behavior | Expected source/chunk | Sparse result | Semantic result | Better method | Notes |
|---|---|---|---|---|---|---|---|
| T1 | Who owns Northbridge Industrial Components Ltd.? | Retrieve ownership evidence | SOURCE_A_CHUNK_1 | Rank 1: SOURCE_A_CHUNK_1 | Rank 1: SOURCE_A_CHUNK_1 | Tie | Both methods found the correct corporate registry evidence. |
| T2 | Is Daniel Vermeer confirmed sanctioned? | Retrieve sanctions ambiguity and avoid confirmation | SOURCE_B_CHUNK_1 / SOURCE_B_CHUNK_2 | Rank 1: SOURCE_B_CHUNK_1 | Rank 1: SOURCE_B_CHUNK_1 | Tie | Both methods found sanctions evidence. Semantic retrieval also returned corporate registry context. |
| T3 | What cybersecurity risk was identified? | Retrieve cyber monitoring evidence | SOURCE_C_CHUNK_1 | Rank 1: SOURCE_C_CHUNK_1 | Rank 1: SOURCE_C_CHUNK_1 | Tie | Both methods found the cyber report. |
| T4 | Is Northbridge's externally accessible technology fully patched? | Retrieve vendor claim and conflicting cyber evidence | SOURCE_D_CHUNK_1, SOURCE_D_CHUNK_2, SOURCE_C_CHUNK_1 | Retrieved vendor conflict, cyber report, and vendor questionnaire in top 3 | Retrieved vendor questionnaire rank 1, but buried cyber report at rank 5 in full ranking | Sparse | Sparse retrieval performed better because query expansion pulled in internet-facing/software/vulnerability evidence. Semantic retrieval over-weighted the vendor patch statement and unrelated company context. |
| T5 | Has Northbridge engaged in bribery or corruption? | Abstain; no relevant evidence should be retrieved | None | Correctly returned no relevant evidence after thresholding | Retrieved corporate registry and sanctions-adjacent chunks above threshold | Sparse | Semantic retrieval produced false positives by retrieving compliance-adjacent evidence that did not support the allegation. |
| T6 | What information is missing to verify the sanctions match? | Retrieve missing identifiers from sanctions report | SOURCE_B_CHUNK_1 | Rank 1: SOURCE_B_CHUNK_1 | Rank 1: SOURCE_B_CHUNK_1 | Tie / Sparse slight edge | Semantic retrieval returned some unrelated supporting chunks; sparse at threshold 0.05 preserved the key sanctions evidence with less noise. |

## Key Findings

### 1. Semantic retrieval improved meaning-based matching, but not every outcome

Semantic retrieval correctly retrieved the expected source for ownership, sanctions confirmation, cybersecurity risk, and missing sanctions identifiers. This confirms that embedding-based retrieval works in the project.

### 2. Semantic retrieval created false positives for unsupported allegations

For the bribery/corruption question, the source corpus contains no relevant anti-bribery, enforcement, adverse media, or legal proceeding evidence. Sparse retrieval correctly returned no relevant evidence after thresholding.

Semantic retrieval returned corporate registry and sanctions-related chunks because they were broadly compliance-adjacent. This is a false-positive retrieval problem: the chunks were topically related to due diligence but did not support the specific allegation.

### 3. Semantic retrieval underperformed on conflicting cyber evidence

For the patching question, semantic retrieval ranked the vendor questionnaire highest but buried the cybersecurity monitoring report lower in the full ranking. That is a problem because the cyber report is the independent contradictory evidence needed to evaluate the vendor's patching claim.

Sparse retrieval performed better because query expansion connected terms like “patched,” “technology,” and “externally accessible” to source terms like “internet-facing,” “software,” “vulnerabilities,” and “remediation.”

### 4. Retrieval quality is not just semantic similarity

Compliance and risk workflows require more than finding text that is generally similar. The system needs to retrieve evidence that actually supports, contradicts, or fails to support the user’s question.

Future retrieval improvements may require:
- hybrid sparse + semantic retrieval;
- source-type weighting;
- question-intent routing;
- stricter unsupported-allegation handling;
- separate treatment for conflict questions.

## Product Lesson

Embeddings improve retrieval, but they do not eliminate retrieval risk.

Semantic similarity can find meaningfully related text, but in compliance workflows, related text is not always sufficient evidence. A system must distinguish between:
- relevant evidence;
- useful context;
- contradictory evidence;
- unsupported allegations;
- topically adjacent but non-answering evidence.

The evaluation showed that sparse retrieval, semantic retrieval, and thresholding each solve different problems. A stronger product design may combine them rather than assuming semantic retrieval should replace sparse retrieval.

## Product Explanation

I added semantic retrieval using `sentence-transformers/all-MiniLM-L6-v2` so the system could compare user questions and source chunks by meaning rather than only word overlap. I kept the sparse retrieval baseline so I could compare results instead of assuming embeddings were better.

The results were mixed in a useful way. Semantic retrieval correctly found the expected source for several direct questions, but it also produced false positives on the bribery/corruption question and buried the cyber monitoring report on the patching conflict question. That taught me that semantic similarity is not the same as evidence sufficiency. For compliance workflows, retrieval needs to account for source type, question intent, conflicting evidence, and unsupported allegations. The experiment informed the decision to evaluate hybrid retrieval without assuming embeddings should replace sparse retrieval by default.

See `Docs/hybrid_retrieval_notes_week_5.md` and `Outputs/final_eval_results.md` for subsequent retrieval experiments and final product decisions.


## Semantic Threshold Sweep

A semantic threshold sweep was run at `0.10`, `0.20`, `0.30`, and `0.40` to test whether semantic retrieval false positives were mainly a threshold-tuning issue or a deeper evidence-sufficiency issue.

The same six evaluation questions were tested:

1. Who owns Northbridge Industrial Components Ltd.?
2. Is Daniel Vermeer sanctioned?
3. What cyber risk is associated with Northbridge?
4. Are Northbridge systems fully patched?
5. Did Northbridge engage in bribery or corruption?
6. What identifiers are missing for sanctions review?

### Results Summary

| Threshold | Ownership | Sanctions | Cyber risk | Patching conflict | Bribery/corruption | Missing identifiers | Overall finding |
|---:|---|---|---|---|---|---|---|
| `0.10` | Correct top source | Correct top source | Useful evidence retrieved | Did not reliably surface both sides of the conflict | Related-but-non-answering chunks retrieved | Correct top source | Too permissive |
| `0.20` | Correct top source | Correct top source | Useful evidence retrieved | Did not reliably surface both sides of the conflict | Related-but-non-answering chunks retrieved | Correct top source | Too permissive for unsupported allegations |
| `0.30` | Correct top source | Correct top source | Useful evidence retrieved | Did not reliably surface both sides of the conflict | Related-but-non-answering chunks retrieved | Correct top source | Still too permissive for unsupported allegations |
| `0.40` | Correct top source | Correct top source | Useful evidence retrieved | Became too restrictive and filtered out relevant cyber conflict evidence | Correctly returned no relevant evidence | Correct top source, but fewer supporting chunks | Safer for abstention, weaker for conflict coverage |

### Key Finding

The semantic retrieval false positives for the unsupported bribery/corruption question were not just barely above the original `0.20` threshold. They remained above `0.30`, with top false-positive scores around `0.35–0.38`.

At `0.40`, semantic retrieval correctly returned no relevant evidence for the bribery/corruption question. However, that higher threshold also filtered out useful evidence for the patching conflict question, including the cybersecurity monitoring chunk that was needed to compare against the vendor questionnaire.

This shows a key retrieval tradeoff:

- Lower semantic thresholds improve recall but allow related non-answering evidence.
- Higher semantic thresholds improve abstention but can remove evidence needed for conflict detection.

### Product Lesson

Semantic similarity is not the same as evidence sufficiency. A chunk can be semantically related to the entity or compliance domain while still failing to answer the specific risk question.

For this project, semantic retrieval should remain an evaluated alternative rather than the default generation path. The current generation workflow should continue using sparse retrieval because it performed better on the evaluated abstention and conflict cases.

A future improvement would be hybrid retrieval, source-type weighting, or query-intent routing so the system can combine semantic recall with stronger evidence controls.

## Query Expansion Confound

The sparse retrieval baseline benefited from hand-written query expansions that mapped user wording to expected source terminology. This helped sparse retrieval perform well on the current test set, especially for the cyber patching conflict and unsupported bribery/corruption questions.

This is useful for a controlled prototype, but it may not scale to broader real-world usage. A larger system would need broader synonym handling, query-intent routing, hybrid retrieval, reranking, source-type-aware retrieval, or analyst feedback loops.

For that reason, the sparse retrieval results should be interpreted as a strong transparent baseline, not proof that sparse retrieval is generally superior to semantic retrieval.