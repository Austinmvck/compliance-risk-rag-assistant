# Compliance Risk RAG Assistant

A source-grounded AI prototype for third-party risk and compliance research.

This project explores how a retrieval-augmented generation workflow can help analysts synthesize evidence from corporate registry, sanctions-screening, cybersecurity-monitoring, and vendor-questionnaire sources while preserving source traceability, abstaining when evidence is insufficient, and routing consequential decisions to human review.

This is an AI/Data Product Management proof artifact, not a production compliance system.

## Project Snapshot

| Area | Description |
|---|---|
| Product | AI-assisted third-party risk research workflow |
| User | Compliance analysts and vendor risk teams |
| Problem | Helping analysts synthesize fragmented risk evidence while preventing unsupported AI conclusions |
| AI Approach | Retrieval-Augmented Generation (RAG) using Claude via Anthropic API |
| Data Sources | Synthetic corporate registry, sanctions, cybersecurity, and vendor questionnaire documents |
| Default Retrieval | Sparse retrieval with threshold-based abstention |
| Evaluation | 15 controlled scenarios covering evidence, ambiguity, conflict, abstention, and decision boundaries |
| Core Product Focus | Evidence grounding, uncertainty handling, citations, and human-review workflows |
| Status | Portfolio prototype; not a production compliance system |

## Project Thesis

The core lesson from the project is:

```text
Correct retrieval does not guarantee correct product behavior.
```

The system performed well when evidence was direct or absent. The hardest cases occurred when relevant evidence existed but required disciplined interpretation.

The final evaluation exposed three post-retrieval product risks:

- a source-scoped sanctions result became a broader clearance claim
- conflicting evidence from different dates was resolved too definitively
- the model rendered a vendor recommendation outside its intended decision authority

The resulting product priorities were:

- claim-scope control
- temporal-uncertainty preservation
- consequential-decision restrictions
- deterministic pre-generation abstention
- human-review guidance

## Target User

The primary user is a compliance or risk analyst reviewing third-party vendors.

Example questions:

- Who owns this company?
- Is this individual associated with sanctions risk?
- Are there unresolved cybersecurity concerns?
- What evidence supports or conflicts with vendor claims?
- Should this case be escalated for human review?

The system is designed to support analyst decision-making, not replace final compliance judgment.

## Start Here

For a fast review, read these files in order:

1. [Architecture Diagram](Docs/architecture_diagram.md) — current generation path, retrieval alternatives, abstention point, and human-review boundary.
2. [System Walkthrough](Docs/system_walkthrough.md) — end-to-end explanation of what happens when a user asks a question.
3. [Final Evaluation Results](Outputs/final_eval_results.md) — scoring methodology, 15-case results, failure analysis, product findings, and limitations.
4. [Final Full Evaluation Output](Outputs/final_full_eval_run_output.md) — complete recorded output for all 15 scenarios.
5. [Product Tradeoffs](Docs/product_tradeoffs.md) — retrieval, scope, safety, and architecture decisions.
6. [Human Review Decision Table](Docs/human_review_decision_table.md) — when the workflow should answer, abstain, or escalate.
7. [Hybrid Retrieval Notes](Docs/hybrid_retrieval_notes_week_5.md) — Reciprocal Rank Fusion experiment and why hybrid retrieval was deferred as the default.

For a short live walkthrough:

- [Final Demo Tests](Outputs/final_demo_tests.md)
- [Recorded Five-Question Demo Output](Outputs/final_demo_run_output.md)
- `Scripts/run_demo_tests.py`

## Problem

Third-party risk research often requires analysts to interpret evidence from multiple sources with different levels of authority, freshness, and completeness.

A relevant source is not always sufficient to support a conclusion.

Examples include:

- an unconfirmed sanctions name match without identity identifiers
- a vendor self-report that conflicts with later external monitoring
- no retrieved evidence for an allegation
- a request for a final vendor approval or risk decision

The prototype was designed to test whether an AI-assisted workflow could:

- retrieve relevant evidence
- preserve source metadata
- answer direct factual questions
- identify ambiguous or conflicting evidence
- abstain when evidence is missing
- avoid treating no evidence as low risk
- cite the evidence used
- route consequential decisions to human review

## Current Workflow

```text
Synthetic source documents
→ metadata extraction
→ sentence-aware chunking
→ processed evidence chunks
→ sparse retrieval
→ minimum similarity threshold
→ retrieved evidence package
→ Claude grounded answer or pre-generation abstention
→ evidence, sources, unknowns, confidence, and human-review guidance
```

The workflow prioritizes evidence sufficiency, traceability, and controlled abstention before generation.

## Retrieval Decision

The current generation path is:

```text
Sparse retrieval
→ thresholding
→ Claude grounded answer or abstention
```

The scoped product decision is:

```text
Sparse retrieval = current generation default
Semantic retrieval = evaluated alternative
Hybrid retrieval = tested with Reciprocal Rank Fusion and deferred
```

### Sparse Retrieval

#### Strengths

- Transparent evidence matching
- Stronger control in tested unsupported-allegation scenarios
- Easier source traceability

#### Limitation

- May miss evidence when user wording differs significantly from source language

#### Decision

Sparse retrieval remains the default generation path for the current workflow.

---

### Semantic Retrieval

#### Strengths

- Improved meaning-based matching
- Better discovery of related concepts

#### Limitations

- Can retrieve related but non-answering evidence
- Semantic relevance does not always equal evidence sufficiency

#### Decision

Semantic retrieval was evaluated but is not used as the default generation path.

---

### Hybrid Retrieval

#### Strengths

- Improved conflict coverage
- Better ability to surface multiple evidence sources

#### Limitations

- Did not fully solve evidence sufficiency
- Increased retrieval complexity without eliminating unsafe evidence scenarios

#### Decision

Hybrid retrieval was tested using Reciprocal Rank Fusion and documented as a targeted future improvement.

## Implemented Capabilities

- Synthetic corporate registry, sanctions, cybersecurity, and vendor-questionnaire corpus.
- Source metadata extraction:
  - source ID
  - source name
  - source date
  - source type
  - entity
- Sentence-aware document chunking.
- Sparse keyword retrieval with query expansion.
- Minimum similarity thresholding.
- Pre-generation abstention when no usable evidence is retrieved.
- Claude answer generation using retrieved evidence only.
- Structured answer output containing:
  - answer
  - evidence used
  - source references
  - unknowns or conflicts
  - confidence
  - human-review guidance
- Semantic retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
- Semantic threshold testing.
- Hybrid retrieval using Reciprocal Rank Fusion.
- Sparse, semantic, and hybrid retrieval comparison on controlled cases.
- Five-question live demo runner.
- Fifteen-question full evaluation runner.
- Captured demo and full-evaluation outputs.
- Structured qualitative scoring and failure taxonomy.
- Architecture, tradeoff, walkthrough, and human-review documentation.

## Evaluation Design

The final evaluation contains 15 controlled scenarios covering:

- direct ownership facts
- beneficial-owner relationships
- ambiguous sanctions matches
- missing identity identifiers
- company sanctions status
- conflicting cyber evidence
- vendor self-reporting
- unsupported bribery and fraud allegations
- inference limits
- vendor approval requests
- overall risk classification

The evaluation assessed:

- required evidence retrieval
- evidence sufficiency
- material-claim support
- source attribution
- abstention behavior
- conflict handling
- human-review routing
- claim scope
- temporal uncertainty
- decision authority

Scoring was performed by the project author against predefined expected behavior and was not independently verified.

This is a controlled qualitative evaluation, not a statistically validated benchmark.

## Evaluation Interpretation

The purpose of the evaluation was not to maximize answer rate.

The goal was to determine whether the system took the correct action:

- Answer when evidence was sufficient
- Abstain when evidence was missing
- Preserve uncertainty when evidence conflicted
- Route high-consequence decisions to human reviewers

A successful AI workflow is not one that always answers.

A successful AI workflow understands when answering is appropriate.

## Final Evaluation Results

All 15 planned scenarios were executed through the sparse generation path.

```text
Pass:    12 / 15
Partial:  3 / 15
Fail:     0 / 15
```

These figures describe author-scored qualitative behavior and should not be interpreted as production accuracy.

### Strongest Behaviors

- Direct factual grounding.
- Source attribution.
- Missing-identifier explanation.
- Sanctions ambiguity handling.
- Conflict retrieval.
- Abstention on unsupported allegations.
- Refusal to infer undisclosed subsidiaries.
- Refusal to issue an unsupported overall low-risk classification.

### Partial Results

#### T6 — Claim-Scope Overclaim

The source said no exact company match was found in the available screening report.

The answer broadened that into:

```text
Northbridge Industrial Components Ltd. is not sanctioned.
```

The retrieval was correct, but the answer exceeded the source scope.

#### T7 — Temporal Over-Resolution

The system retrieved both:

- an April vendor self-report that systems were patched
- a May monitoring report identifying one outdated internet-facing service

The answer concluded broadly that Northbridge systems were not fully patched.

The response did not fully preserve the difference between:

- earlier state
- later observed state
- current unknown state
- one affected service
- the complete system estate

#### T14 — Decision Overreach

The system retrieved the correct vendor and cyber evidence, identified the conflict, stated unknowns, and required human review.

However, it still recommended that the vendor not be approved.

The assistant was intended to support an analyst, not render the final vendor decision.

## Cross-Scenario Findings

### Direct Evidence and Abstention Were Strong

The workflow behaved reliably when:

- explicit source text answered the question
- no relevant evidence was available

For unsupported bribery, fraud, subsidiary, and overall-risk questions, thresholding blocked Claude before generation.

This made abstention a system control rather than a prompt-only request.

### Relevant Evidence Can Still Produce Unsafe Output

T6, T7, and T14 all retrieved relevant evidence.

The remaining issues occurred after retrieval:

```text
correct evidence
≠ correctly scoped claim
≠ correctly timed conclusion
≠ authorized decision
```

The product therefore needs to evaluate not only retrieval and grounding, but whether the system took the correct action.

## Product Controls Added From Evaluation Findings

The evaluation findings were converted into product requirements and system controls rather than treated as isolated model failures.

The controls focused on preventing three categories of unsafe AI behavior:

- unsupported claim expansion
- incorrect resolution of conflicting evidence
- decisions outside model authority

### Claim-Scope Control

When a source reports no match, the answer should describe the scope of that source and screening result rather than implying universal clearance.

### Temporal-Conflict Control

When evidence differs across dates, the answer should separate:

- earlier evidence
- later evidence
- current unknown state

### Consequential-Decision Control

The system should not:

- approve vendors
- reject vendors
- issue sanctions clearance
- assign final risk classifications

It should:

- summarize evidence
- identify unresolved risks
- state missing information
- recommend follow-up evidence
- route the decision to an authorized human reviewer

### Post-Generation Policy Evaluation

A future policy check should detect whether an answer:

- exceeds source scope
- ignores temporal limits
- treats absence of evidence as proof
- makes a prohibited final decision
- cites evidence that does not support the claim

## Implemented Reliability Improvements

The initial evaluation findings were converted into explicit controls, regression checks, and reproducibility improvements.

Implemented changes:

- Added fail-fast execution behavior so model/API failures cannot produce false successful evaluations.
- Added deterministic sparse retrieval regression tests covering:
  - ownership evidence retrieval
  - sanctions evidence retrieval
  - conflicting source retrieval
  - unsupported allegation abstention
  - evidence provenance fields
- Added prompt controls for:
  - evidence scope limitations
  - temporal uncertainty
  - human decision boundaries
- Added reproducibility controls:
  - Python 3.12 runtime declaration
  - bounded dependency versions
  - GitHub Actions validation workflow
  - v1.0-portfolio release tag

The goal was not to eliminate uncertainty from AI outputs, but to design a workflow where uncertainty is visible, evidence remains traceable, and unresolved decisions are routed to appropriate human reviewers.

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/Austinmvck/compliance-risk-rag-assistant.git
cd compliance-risk-rag-assistant
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Anthropic API key

```bash
cp .env.example .env
```

Then replace the placeholder in `.env`:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Do not commit `.env`.

### 5. Build processed chunks

```bash
python3 Scripts/03_build_chunks.py
```

### 6. Run a single grounded question

```bash
python3 Scripts/05_rag_answer.py "Is Daniel Vermeer sanctioned?"
```

### 7. Run the five-question demo

```bash
python3 Scripts/run_demo_tests.py
```

### 8. Run the full 15-question evaluation

```bash
python3 Scripts/run_full_evaluation.py
```

To capture a new run:

```bash
python3 Scripts/run_full_evaluation.py > Outputs/final_full_eval_run_output.md
```

Model responses can vary across repeated runs.

## Repository Guide

### Core Scripts

- `Scripts/03_build_chunks.py` — parses source documents and creates metadata-preserving chunks.
- `Scripts/04_retrieve_chunks.py` — sparse keyword retrieval and thresholding.
- `Scripts/05_rag_answer.py` — current generation path and pre-generation abstention.
- `Scripts/06_semantic_retrieve_chunks.py` — semantic embedding retrieval.
- `Scripts/07_hybrid_retrieve_chunks.py` — hybrid Reciprocal Rank Fusion experiment.
- `Scripts/run_demo_tests.py` — five representative interview/demo scenarios.
- `Scripts/run_full_evaluation.py` — complete 15-scenario evaluation runner.

### Data

- `Data/sources/` — synthetic source documents.
- `Data/processed_chunks.json` — processed evidence chunks with metadata.

### Core Documentation

- `Docs/architecture_diagram.md`
- `Docs/system_walkthrough.md`
- `Docs/product_tradeoffs.md`
- `Docs/human_review_decision_table.md`
- `Docs/retrieval_evaluation_matrix_week_4.md`
- `Docs/hybrid_retrieval_notes_week_5.md`

### Evaluation Outputs

- `Outputs/final_demo_tests.md`
- `Outputs/final_demo_run_output.md`
- `Outputs/final_full_eval_run_output.md`
- `Outputs/final_eval_results.md`

## What This Project Demonstrates

- Source-grounded AI workflow design.
- Metadata-preserving document processing.
- Retrieval-method experimentation.
- Evidence-sufficiency evaluation.
- Threshold-based abstention.
- Source traceability.
- Conflicting-evidence handling.
- Human-review and decision-boundary design.
- Failure taxonomy development.
- AI product tradeoff analysis.
- Translation of evaluation findings into product controls.

## Intentionally Out of Scope

The project does not include:

- production deployment
- a user interface
- authentication or multi-user access
- real customer or vendor data
- automated final compliance decisions
- replacement of human analysts
- production monitoring or security controls
- automatic citation verification
- a production vector database
- model training or fine-tuning
- production case-management or reviewer-routing workflows
- autonomous agent orchestration

These items were excluded to keep the v1 artifact focused on retrieval behavior, evidence interpretation, abstention, evaluation, and product controls.

## Limitations

- The corpus is small and synthetic.
- The evaluation is author-scored and not independently verified.
- The 15 scenarios are controlled and not statistically representative.
- Several questions reuse the same underlying source facts.
- The full 15-case evaluation was run through the sparse generation path, not all three retrieval methods.
- Results depend on the current corpus, threshold, prompt, and model version.
- Model output may vary across repeated runs.
- Citation references are displayed but not automatically verified.
- Human-review behavior is represented in responses, not implemented as a production workflow.
- The project does not evaluate production latency, cost, security, multilingual behavior, adversarial prompting, or large-corpus performance.

## Potential V2 Improvements

- Machine-readable evaluation dataset.
- Repeated trials to measure model variability.
- Required, optional, and distractor-chunk labels.
- Retrieval recall and complete-evidence coverage metrics.
- Abstention precision and recall.
- Claim-level citation verification.
- Temporal-reasoning tests.
- Prohibited-decision detection.
- Post-generation policy evaluation.
- Full 15-case semantic and hybrid comparisons.
- Independent or blinded scoring.

These are future maturity improvements, not requirements for the completed v1 artifact.

## Production Considerations

A production implementation would require additional controls beyond this prototype:

- larger and continuously refreshed data sources
- source authority ranking
- automated citation validation
- model and retrieval monitoring
- security and access controls
- human-review workflow integration
- audit logging
- evaluation regression pipelines
- cost and latency optimization

The prototype focuses on demonstrating product judgment around evidence grounding, uncertainty handling, and decision boundaries before production scaling.

## Project Status

```text
V1 prototype and structured evaluation complete.
```

The project is now in packaging and interview-use mode rather than active feature development.
