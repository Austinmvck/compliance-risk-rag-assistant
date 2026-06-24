# Week 3 Retrieval Notes

## Summary

This week moved the artifact from controlled-context grounding to a minimal retrieval-augmented generation workflow.

The system now:
- loads multiple source documents,
- splits them into chunks,
- preserves source metadata,
- retrieves relevant chunks based on a user question,
- sends retrieved evidence to Claude,
- produces a grounded answer with source references.

## Retrieval Baseline

The first retrieval baseline used lightweight term-frequency similarity and cosine scoring.

This approach was transparent and easy to inspect, but it had limitations:
- user wording did not always match source wording,
- common entity terms created noise,
- zero-score chunks could still be returned,
- the system did not distinguish primary evidence from secondary references,
- character-based chunking could split words or claims.

## Retrieval Iteration

The initial cyber conflict query failed to retrieve the Cybersecurity Monitoring Report. It retrieved the Vendor Questionnaire plus irrelevant Corporate Registry and Sanctions chunks.

The likely cause was vocabulary mismatch:
- user wording: "externally accessible technology fully patched"
- source wording: "internet-facing file-transfer service using outdated software"

A lightweight query-expansion step improved retrieval by mapping business terms to domain-specific source terms.

After the update, the cyber conflict question retrieved both:
- Vendor Questionnaire
- Cybersecurity Monitoring Report

## RAG Answer Tests

### Test 1: Direct Fact

The ownership question retrieved Corporate Registry evidence and produced a grounded answer.

### Test 2: Conflicting Evidence

The patching question retrieved both vendor and cyber monitoring evidence. Claude surfaced the conflict and recommended verification.

### Test 3: Missing Evidence / Abstention

The bribery/corruption question retrieved no supportive evidence. Claude stated insufficient evidence and avoided making an unsupported allegation.

## Current Limitations

- Retrieval is still keyword/query-expansion based, not embedding-based semantic retrieval.
- Query expansion is manually defined and brittle.
- The script always returns top 3 chunks, even when scores are zero.
- Character-based chunking can split words and related facts.
- Source references are model-generated and not automatically verified.
- The source corpus is small and synthetic.
- No formal retrieval score threshold exists yet.
- No architecture diagram or final README update has been completed yet.

## Product Lessons

1. RAG quality depends heavily on retrieval quality, not just model quality.
2. User wording may differ from source wording, creating retrieval failures.
3. Retrieved evidence must be inspected before generation to diagnose failures.
4. Similarity score is a ranking signal, not factual confidence.
5. Missing-evidence questions require abstention, not speculation.
6. Compliance and risk workflows require source provenance, conflict handling, and human review.

## Next Improvements

- Add a minimum similarity threshold.
- Improve chunking to avoid splitting words or claims.
- Consider embedding-based semantic retrieval.
- Save evaluation outputs in a structured table.
- Update README to reflect the new RAG workflow.
- Add a human-review decision framework.
