# System Walkthrough

## Purpose

This document walks through how the Compliance Risk RAG Assistant handles a user question from start to finish.

The goal is to explain the runtime workflow: how the system receives a question, retrieves evidence, applies evidence controls, decides whether to call Claude, generates a grounded answer, and routes cases to human review when needed.

This walkthrough reflects the current prototype. It does not describe a production workflow.

## Block 3 Lesson

The main lesson from this block is that a RAG system is not just retrieval plus generation.

A safer risk workflow needs decision points:

```text
User question
→ evidence retrieval
→ evidence quality gate
→ Claude or abstention
→ grounded answer
→ human review when needed
```

The product value is not only that the model can answer. The product value is that the workflow controls when the model should answer, when it should abstain, and when a human analyst should review the case.

This matters because risk and compliance questions can involve missing evidence, stale evidence, conflicting sources, or high-consequence decisions. The system should not treat every retrieved chunk as sufficient evidence.

## High-Level Workflow

```text
1. User asks a third-party risk question.
2. The system loads processed evidence chunks from Data/processed_chunks.json.
3. Sparse retrieval ranks chunks against the user question.
4. Similarity thresholding filters weak or irrelevant matches.
5. If no relevant evidence is found, the system abstains before generation and Claude is not called.
6. If relevant evidence is found, the retrieved evidence package is sent to Claude.
7. Claude generates a grounded answer using only the retrieved evidence.
8. The answer includes evidence used, unknowns, limitations, caution, and human-review guidance.
9. Ambiguous, conflicting, unsupported, or high-consequence cases are routed to human review.
```

## Source Corpus

The prototype uses a small synthetic third-party risk source corpus about Northbridge Industrial Components Ltd.

The source documents include:

- Corporate Registry Extract
- Sanctions Screening Report
- Cybersecurity Monitoring Report
- Vendor Questionnaire

These sources were designed to test different risk research behaviors:

- direct factual lookup
- ambiguous sanctions evidence
- conflicting cyber evidence
- vendor self-report limitations
- unsupported allegations
- missing information

The corpus is intentionally synthetic. It is not real vendor or customer data.

## Step 1 — User Asks a Question

The user asks a risk or compliance research question, such as:

```text
Who owns Northbridge Industrial Components Ltd.?
```

or:

```text
Are Northbridge systems fully patched?
```

or:

```text
Did Northbridge engage in bribery or corruption?
```

Different questions require different evidence behavior.

An ownership question is usually a direct evidence lookup from the corporate registry.

A patching question is harder because it may require comparing multiple sources across time. The vendor questionnaire says external systems were patched as of April 15, while the later cybersecurity monitoring report says an internet-facing file-transfer service still used outdated software on May 5.

An unsupported bribery or corruption question requires abstention if no source provides evidence for the allegation.

## Step 2 — Load Processed Chunks

The system loads processed chunks from:

```text
Data/processed_chunks.json
```

These chunks are created from the source documents by:

- extracting metadata
- preserving source context
- splitting documents into sentence-aware chunks

Each chunk preserves metadata such as:

- source ID
- source name
- source type
- source date
- entity
- chunk ID

This matters because a grounded answer should identify not only what the evidence says, but where it came from.

## Step 3 — Retrieve Evidence

The current generation path uses sparse retrieval:

```text
Scripts/04_retrieve_chunks.py
```

Sparse retrieval compares the user question against the processed chunks using term overlap and query expansion logic.

The goal is to identify chunks that are most relevant to the question.

Example:

For the question:

```text
Who owns Northbridge Industrial Components Ltd.?
```

Sparse retrieval should return corporate registry evidence that identifies the ownership structure.

For the question:

```text
Are Northbridge systems fully patched?
```

Sparse retrieval should retrieve evidence from both the Vendor Questionnaire and Cybersecurity Monitoring Report if the wording and thresholding support the match.

## Step 4 — Apply Thresholding

After retrieval, the system applies a similarity threshold.

This threshold acts as an evidence quality gate.

If retrieved chunks do not meet the threshold, they should not be passed to Claude.

This matters because weakly related chunks can create unsupported answers. In a risk workflow, adjacent or entity-related evidence is not always sufficient evidence.

## Step 5 — Decide Whether to Call Claude

The system decides whether Claude should be called.

There are two paths:

```text
Relevant evidence found → call Claude with retrieved evidence package
No relevant evidence found → abstain before generation and do not call Claude
```

This is an important control.

Claude should not be asked to answer from weak, missing, or irrelevant evidence. The system should enforce abstention before generation instead of relying only on prompt instructions.

No evidence found does not mean low risk. It means the available source corpus does not contain sufficient evidence to answer the question.

## Step 6 — Generate Grounded Answer

When relevant evidence is found, the system calls Claude using:

```text
Scripts/05_rag_answer.py
```

Claude receives the retrieved evidence package, not the full source corpus.

The answer should be grounded in the provided evidence and should avoid claims that are not supported by the retrieved chunks.

The system should not allow Claude to invent missing details, confirm allegations without evidence, or make final compliance decisions.

## Step 7 — Return Evidence, Unknowns, and Caution

The grounded answer should include:

- direct answer when supported
- evidence used
- source references
- unknowns or missing information
- limitations
- caution level
- human-review guidance when needed

This structure matters because third-party risk research often depends on what is known, what is unknown, and what still requires analyst verification.

## Step 8 — Route Human Review When Needed

Human review is needed when the system identifies:

- possible sanctions matches
- missing identifiers
- conflicting evidence
- unsupported allegations
- vendor self-report without supporting evidence
- stale source data
- low retrieval confidence
- high-consequence onboarding, renewal, escalation, or compliance decisions

The system supports analyst judgment. It does not replace analyst judgment.

## Walkthrough Example 1 — Ownership

### User Question

```text
Who owns Northbridge Industrial Components Ltd.?
```

### Expected Evidence

The Corporate Registry Extract contains ownership evidence.

### Workflow

```text
Question
→ load processed chunks
→ sparse retrieval finds corporate registry chunk
→ threshold passes
→ Claude receives ownership evidence
→ Claude answers with source-grounded ownership summary
```

### Expected Behavior

The system should answer that Northbridge is owned by:

- Northbridge Holdings B.V. at 70%
- Daniel Vermeer at 20%
- private investors at 10%

The answer should reference the corporate registry evidence and avoid adding ownership claims not present in the source.

### Human Review

Human review may not be required for the basic ownership lookup, but an analyst may still review if ownership is used for onboarding, sanctions escalation, or compliance decisions.

## Walkthrough Example 2 — Sanctions Ambiguity

### User Question

```text
Is Daniel Vermeer sanctioned?
```

### Expected Evidence

The Sanctions Screening Report contains ambiguous evidence.

It says there is no exact company match, but there is a possible Daniel Vermeer match to an EU restrictive-measures individual. The match is not confirmed because key identifiers are missing.

### Workflow

```text
Question
→ sparse retrieval finds sanctions screening evidence
→ threshold passes
→ Claude receives sanctions evidence
→ Claude answers with caution and missing identifiers
→ human review required
```

### Expected Behavior

The system should not confirm that Daniel Vermeer is sanctioned.

It should say that there is a possible name match that requires verification and that missing identifiers prevent confirmation.

### Human Review

Human review is required because possible sanctions matches are high consequence and cannot be resolved from name similarity alone.

## Walkthrough Example 3 — Cyber Patching Conflict

### User Question

```text
Are Northbridge systems fully patched?
```

### Expected Evidence

The answer requires comparing two sources:

- Vendor Questionnaire
- Cybersecurity Monitoring Report

The Vendor Questionnaire says external systems were patched as of April 15.

The Cybersecurity Monitoring Report says that on May 5, an internet-facing file-transfer service still used outdated software with known public vulnerabilities.

### Workflow

```text
Question
→ sparse retrieval searches processed chunks
→ relevant vendor and cyber evidence is retrieved
→ threshold passes
→ Claude receives evidence package
→ Claude identifies conflict between sources
→ human review recommended
```

### Expected Behavior

The system should not simply answer “yes.”

A better answer is that the evidence is conflicting. The vendor self-reported patching as of April 15, but later external cyber monitoring found outdated software on May 5.

### Human Review

Human review is needed because the sources conflict and because cyber remediation status can affect risk decisions.

## Walkthrough Example 4 — Unsupported Bribery/Corruption

### User Question

```text
Did Northbridge engage in bribery or corruption?
```

### Expected Evidence

The current source corpus does not contain evidence supporting a bribery or corruption allegation.

### Workflow

```text
Question
→ sparse retrieval searches processed chunks
→ no sufficient evidence is found
→ system abstains before generation
→ Claude is not called
```

### Expected Behavior

The system should not answer the allegation from adjacent compliance or corporate registry evidence.

It should abstain and explain that the available evidence does not support a conclusion.

### Human Review

Human review may be needed if the question is part of a real investigation, but the system should not treat missing evidence as proof of low risk.

## What the System Does Not Do

The system does not:

- make final compliance decisions
- confirm sanctions matches without identifiers
- prove low risk from missing evidence
- automate vendor onboarding decisions
- automate renewal decisions
- replace analyst review
- use real customer or vendor data
- run as a production application
- include a user interface
- include authentication or multi-user access
- use a production vector database
- deploy agents

This prototype is designed to demonstrate source-grounded AI workflow design, not production readiness.

## Product Lesson

The main product lesson is that evidence workflow design matters as much as model output.

For third-party risk and compliance use cases, the system must distinguish between:

- evidence that directly answers the question
- evidence that is related but non-answering
- evidence that is missing
- evidence that conflicts
- evidence that requires human verification

The system should only answer when evidence is sufficient. Otherwise, it should abstain or route to human review.

## Interview Explanation

The walkthrough starts with a user question, then loads processed chunks that preserve source metadata. The current path uses sparse retrieval to identify relevant evidence. The system applies thresholding before generation, so Claude is only called if relevant evidence is found.

Claude receives the retrieved evidence package, not the full source corpus. The answer includes evidence used, unknowns, limitations, caution, and human-review guidance.

If the evidence is missing, conflicting, ambiguous, or high consequence, the system abstains or routes to human review instead of making a final compliance decision.