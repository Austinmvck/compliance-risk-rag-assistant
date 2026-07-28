# Post-Control Evaluation Scorecard

## Overview

This document summarizes the post-control evaluation results after implementing targeted product controls for:

- Claim scope
- Temporal and conflict handling
- Decision authority boundaries
- Human-review routing
- Abstention behavior

The goal of the evaluation was not to measure whether the model could generate answers. The goal was to evaluate whether the system made the correct product decision:

- Answer when evidence was sufficient
- Qualify when evidence was limited or conflicting
- Abstain when evidence was missing
- Escalate when human judgment was required

---

# 1. Final Results

## Overall Scorecard

| Rating | Initial Evaluation | Post-Control Evaluation | Change |
|---|---:|---:|---:|
| Pass | 12 | 15 | +3 |
| Partial | 3 | 0 | -3 |
| Fail | 0 | 0 | 0 |
| Total | 15 | 15 | — |

The three original Partial cases were:

- **T6 — Company sanctions status**
- **T7 — Cyber patching conflict**
- **T14 — High-consequence vendor decision**

These cases represented the highest product-risk scenarios because they involved interpretation boundaries rather than simple retrieval.

---

## Partial → Pass Improvements

### T6 — Company sanctions status

**Original issue**

The system converted a source-scoped sanctions screening result into a broader conclusion that Northbridge was not sanctioned.

**Product risk**

This created a false sense of clearance by implying the available evidence was sufficient to make a universal sanctions determination.

**Control added**

Claim scope control:

- Keep statements limited to what the retrieved evidence supports.
- Avoid converting "no match found in this report" into "not sanctioned."

**Post-control behavior**

The system now states that:

- No exact company sanctions match was identified in the retrieved report.
- The report does not confirm sanctions.
- Additional review may still be required.

**Why Pass**

The response distinguishes between:

- "Not identified in retrieved evidence"
- "Confirmed not sanctioned"

These are materially different compliance conclusions.

**Remaining limitation**

The answer still depends on:

- Screening provider coverage
- Data freshness
- Scope of sanctions lists reviewed
- Human verification for unresolved cases

---

### T7 — Cyber Patching Conflict

**Original issue**

The system over-generalized conflicting evidence by stating that Northbridge systems were not fully patched.

**Product risk**

A conflict between sources should not automatically become a definitive conclusion. The system must preserve uncertainty and identify what requires verification.

**Control added**

Conflict-handling controls:

- Preserve source dates
- Identify conflicting evidence
- Maintain asset scope
- Identify unresolved questions
- Recommend next verification steps

**Post-control behavior**

The system now explains:

- Vendor questionnaire stated external systems were patched as of April 15.
- Cyber monitoring later identified outdated software on an internet-facing file-transfer service.
- The scope of the conflict is unknown.
- Current remediation status requires confirmation.

**Why Pass**

The system no longer chooses a side without enough evidence.

It preserves:

- Evidence
- Timeline
- Source differences
- Unknowns
- Next actions

**Remaining limitation**

The system does not currently:

- Rank source reliability formally
- Calculate confidence scores
- Validate remediation automatically

---

### T14 — High-Consequence Vendor Decision

**Original issue**

The system crossed the authority boundary by making a vendor approval recommendation.

**Product risk**

High-consequence business decisions should not be delegated to an AI system without appropriate human governance.

**Control added**

Decision-authority control:

- Summarize evidence
- Identify risks
- Identify unknowns
- Route final approval decisions to authorized reviewers

**Post-control behavior**

The system now states:

- Available evidence does not support immediate approval.
- Conflicting security evidence exists.
- Additional review is required.

**Why Pass**

The system provides decision support without pretending to own the final business decision.

**Remaining limitation**

The prototype does not include:

- Formal approval workflows
- Reviewer assignment
- Audit tracking
- Escalation SLAs

---

# 2. Behavioral Evaluation Results

| Behavior | Result |
|---|---:|
| Supported-answer handling | Pass |
| Missing evidence abstention | Pass |
| Conflict preservation | Pass |
| Citation support | Pass |
| Claim scope control | Pass |
| Human-review routing | Pass |
| Temporal uncertainty handling | Pass |

---

# 3. Final Evaluation Statement

All 15 post-control scenarios passed the defined qualitative evaluation rubric.

Within the controlled synthetic test set:

- Supported answers remained grounded in retrieved evidence.
- Unsupported questions triggered abstention.
- Conflicting evidence was preserved instead of over-resolved.
- Citations supported material claims.
- Source and date limitations remained visible.
- High-consequence decisions remained with human reviewers.

This does **not** represent production readiness or proof of perfect AI accuracy.

The evaluation demonstrates that the implemented controls improved system behavior within the defined scenarios.

---

# 4. Findings and Product Conclusion

## Finding 1 — Retrieval relevance is not enough

The evaluation showed that retrieving related evidence does not guarantee safe AI behavior.

A system can retrieve relevant information but still:

- Overstate conclusions
- Ignore uncertainty
- Make decisions outside its authority

The product challenge is not only finding evidence.

The product challenge is controlling how evidence is interpreted.

---

## Finding 2 — Claim scope is a critical AI safety control

The system needed explicit controls to prevent:

- Narrow evidence becoming broad conclusions
- "No evidence found" becoming "evidence disproves"
- Screening results becoming universal clearance

High-trust AI workflows require clear boundaries between:

- What is known
- What is supported
- What remains unknown

---

## Finding 3 — Conflict handling requires chronology and context

The cyber patching scenario demonstrated that conflicting sources cannot simply be merged into one answer.

The system must preserve:

- Source type
- Date
- Scope
- Confidence
- Unknowns

The correct product behavior is often not selecting the "true" answer.

The correct behavior is explaining why the evidence is unresolved.

---

## Finding 4 — Human review is a product capability

Human review should not be viewed as a failure mode.

For high-consequence workflows, escalation is part of the product design.

The system should know when:

- Evidence is insufficient
- Sources conflict
- Decisions exceed AI authority

---

# 5. Remaining Limitations

## Synthetic evaluation data

The evaluation uses a controlled synthetic corpus.

It does not represent:

- Real vendor documents
- Real compliance workflows
- Real analyst behavior
- Real-world data ambiguity

---

## No independent validation

The evaluation was designed and reviewed by the project author.

Future validation would require:

- Compliance analyst review
- Independent scoring
- Reviewer agreement measurement

---

## No formal source reliability model

The system preserves source metadata but does not formally score:

- Source credibility
- Historical accuracy
- Reliability by document type

---

## Limited entity resolution testing

The prototype does not deeply evaluate:

- Name matching
- Alias resolution
- Ownership chains
- False positive rates
- False negative rates

---

## No live freshness controls

The current system does not include production controls for:

- Data refresh
- Document versioning
- Expired evidence
- Watchlist updates
- Source monitoring

---

## Limited operational workflow testing

Human review logic exists conceptually but has not been measured through:

- Reviewer agreement
- Escalation accuracy
- Review time
- Override rates
- Analyst productivity impact

---

## No production deployment

The prototype does not include:

- Authentication
- Authorization
- Infrastructure monitoring
- Cost monitoring
- Production logging
- Model drift monitoring

---

# 6. Product Conclusion

The final evaluation demonstrates that the prototype became better at making the correct AI workflow decision:

| Situation | Correct Behavior |
|---|---|
| Evidence is sufficient | Answer |
| Evidence is incomplete | Qualify |
| Evidence conflicts | Preserve uncertainty |
| Evidence is missing | Abstain |
| Decision is high consequence | Escalate |

The largest improvement was not retrieval performance.

The largest improvement was adding product controls that govern how evidence becomes decisions.

The final system demonstrates an interview-credible approach to building AI products for high-trust workflows:

- Evidence grounding
- Retrieval evaluation
- Failure analysis
- Human-in-the-loop design
- Risk-aware product decisions

It demonstrates product judgment around AI reliability, not production deployment readiness.

---

# 7. Interview Takeaway

## 30-Second Version

I built a compliance-risk RAG prototype to test how an AI product should answer questions from source documents while preserving evidence traceability, abstaining when support is insufficient, and routing consequential decisions to human review.

The biggest lesson was that retrieval alone does not create trustworthy AI. The product needed controls around claim scope, uncertainty, conflicting evidence, and decision authority.

---

## 2-Minute Version

I built a compliance-risk RAG assistant focused on third-party risk research.

The initial system could retrieve evidence and generate grounded answers, but evaluation exposed three important product risks:

1. The system could overstate narrow evidence.
2. The system could over-resolve conflicting sources.
3. The system could cross into decisions that required human authority.

I added controls for:

- Claim scope
- Conflict handling
- Temporal reasoning
- Abstention
- Human-review routing

After applying those controls, all 15 evaluation scenarios passed the defined rubric.

The biggest lesson was that AI product quality is not just about getting the answer. It is about knowing when the system should answer, qualify, abstain, or escalate.

---

## 5-Minute Version

The project explored how to design an AI workflow for high-trust compliance research.

The system included:

- Document processing
- Metadata preservation
- Retrieval evaluation
- Sparse, semantic, and hybrid retrieval experiments
- Evidence grounding
- Citation traceability
- Abstention controls
- Human-review workflows
- Evaluation scenarios

The first evaluation produced:

- 12 Pass
- 3 Partial
- 0 Fail

The Partial cases were valuable because they exposed product failures.

T6 showed that evidence scope matters.

T7 showed that conflicting evidence requires chronology and uncertainty.

T14 showed that AI systems need explicit decision boundaries.

After implementing controls, the system achieved:

- 15 Pass
- 0 Partial
- 0 Fail

The biggest takeaway was that safer AI behavior came from product controls, not simply from improving retrieval.

The next production steps would include:

- Larger evaluation sets
- Independent review
- Source reliability scoring
- Better entity resolution
- Freshness controls
- Production monitoring

The project demonstrates how a Product Manager can approach AI systems through evidence quality, workflow design, evaluation, and governance.
