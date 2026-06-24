# Week 3 Retrieval Plan

## Objective

Move the artifact from controlled-context grounding to a minimal retrieval-augmented generation workflow.

The system should accept a user question, search across multiple source documents, retrieve the most relevant source chunks, display those chunks with metadata, and send only the retrieved evidence to Claude.

The purpose of this phase is to evaluate retrieval independently from generation.

## Definition of Done

This milestone is complete when:

1. Multiple source documents are loaded separately.
2. Documents are divided into chunks with source metadata.
3. A user question is converted into a searchable representation.
4. Source chunks are ranked by semantic relevance.
5. The top retrieved chunks are printed before generation.
6. Only the retrieved chunks are sent to Claude.
7. Claude produces a grounded answer with source references.
8. Retrieval and generation failures can be evaluated separately.

## Initial Retrieval Test Set

| Test ID | Question | Expected Source(s) | Expected Retrieval Behavior | Expected Answer Behavior |
|---|---|---|---|---|
| R1 | Who owns Northbridge Industrial Components Ltd.  | Corporate Registry | Corporate ownership information should rank first or within top 3 | Summarize ownership without adding unsupported details |
| R2 | Is Daniel Vermeer confirmed to be sanctioned? | Sanctions Screening Report | Sanctions report should rank first | State that the match is possible but unconfirmed |
| R3 | What cybersecurity risk was identified? | Cybersecurity Monitoring Report | Cyber monitoring source should rank first | Identify outdated software and avoid claiming a confirmed breach |
| R4 | Is Northbridge’s externally accessible technology fully patched? | Cybersecurity Monitoring Report and Vendor Questionnaire | Both conflicting sources should appear within top results | Surface the contradiction and recommend verification |
| R5 | Has Northbridge engaged in bribery or corruption that is supported on a Government or NGO list? | No source directly supports the claim | Retrieval may return weakly related content, but no highly relevant evidence should exist | State insufficient evidence and avoid an allegation |
| R6 | What information is missing to verify the sanctions match? | Sanctions Screening Report | Sanctions source should rank first | Identify missing date of birth, passport, nationality, or other identifiers |

## Retrieval Success Criteria

### Minimum Success

- The expected source appears within the top 3 retrieved chunks for direct-evidence questions.
- The top-ranked chunk is relevant to the question in at least 4 of the 6 initial tests.
- Source name, date, document type, and chunk identifier remain visible.
- The retrieved evidence changes when the question changes.
- Missing-evidence questions do not produce a confident unsupported answer.

### Strong Success

- The expected source ranks first for direct fact questions.
- Both relevant sources appear for the conflicting-evidence question.
- Irrelevant sources do not dominate the top 3 results.
- Claude uses only the retrieved evidence.
- Source references in the answer correspond to the retrieved chunks.

### Current Limitations

- Small synthetic dataset.
- No calibrated similarity threshold.
- No production vector database.
- No automated citation verification.
- Limited number of evaluation questions.
- Retrieval quality may appear artificially high because the source collection is small.

## Failure Taxonomy

### Retrieval Failure

The correct evidence exists in the source collection but is not retrieved within the top results.

Example:
The ownership question fails to retrieve the corporate registry.

### Ranking Failure

The correct evidence is retrieved, but irrelevant evidence ranks above it.

Example:
The vendor questionnaire ranks above the sanctions report for a sanctions question.

### Coverage Failure

The question requires multiple sources, but the system retrieves only one.

Example:
The patching question retrieves the vendor questionnaire but not the external monitoring report.

### Missing-Evidence Failure

The source collection does not contain the answer, but the retrieved content appears relevant enough to encourage an unsupported conclusion.

### Generation Failure

The correct evidence is retrieved, but Claude misstates, ignores, or exaggerates it.

### Traceability Failure

The answer includes a claim but does not identify the source that supports it.

## Initial Retrieval Configuration

### Chunking

Initial approach:

- Paragraph-based or fixed-size chunks
- Approximately 500–800 characters per chunk
- Approximately 100–150 characters of overlap
- Metadata attached to every chunk

This is an initial test configuration, not an assumed best practice.

### Retrieval

Initial approach:

- Semantic similarity using embeddings
- Return the top 3 chunks
- Print similarity score and metadata before generation

### Metadata

Each chunk should preserve:

- source ID
- source name
- source date
- source type
- entity
- chunk ID
- original text

### Product Tradeoffs

- Larger chunks preserve context but may include irrelevant information.
- Smaller chunks improve precision but may separate related facts.
- Higher top-k improves coverage but introduces noise and increases cost.
- Similarity scores indicate semantic closeness, not factual certainty.
- Retrieval confidence should not be presented to users as model confidence.

## PM Decision

Controlled-context grounding was tested before retrieval so that model behavior could be evaluated with known evidence.

The next phase introduces retrieval as a separate system component. This allows failures to be diagnosed more accurately:

- Did the system find the right evidence?
- Did the model use the evidence correctly?
- Did the workflow preserve uncertainty and traceability?

The system will remain local and lightweight until the retrieval loop is proven. A hosted vector database, frontend, agents, and production deployment are intentionally out of scope.

## Decisions Before Implementation

1. I will start with top 3 retrieved chunks because the source set is small and I want enough coverage to catch conflicting evidence without flooding the model with irrelevant text.

2. I will print retrieved chunks before sending them to Claude so retrieval quality can be inspected separately from answer quality.

3. I will preserve source name, date, type, and chunk ID because source traceability is required for compliance and risk workflows.

4. I will keep the implementation local and lightweight because the current goal is to prove the retrieval loop, not production infrastructure.

5. I will treat similarity score as a ranking signal, not as factual confidence.

## Retrieval Baseline Findings

The first keyword-based retrieval baseline successfully retrieved the correct source for ownership and sanctions questions.

The initial version failed the cybersecurity conflict question because corporate registry and sanctions chunks ranked above the relevant cyber monitoring source. This showed that user wording such as "externally accessible technology fully patched" did not match the source wording "internet-facing file-transfer service using outdated software."

A lightweight query expansion improved retrieval. After expansion, the cyber conflict question retrieved both the vendor questionnaire and the cybersecurity monitoring report in the top 3.

Remaining limitations:
- Query expansion is manually defined and brittle.
- The script always returns top 3 chunks even if some scores are weak or zero.
- The system does not yet distinguish primary evidence from secondary references.
- Character-based chunking can split words and over-rank short dense fragments.
- This is not yet embedding-based semantic retrieval.