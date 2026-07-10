# Final Demo Tests

## Purpose

This document defines the final demo test set for the Compliance Risk RAG Assistant.

The goal is to show how the prototype behaves across supported, ambiguous, conflicting, partially answerable, and unsupported third-party risk questions.

This is not a production evaluation suite. It is a focused demo/evaluation table designed to make the system easier to test, explain, and discuss in interviews.

## Week 6 Block 1 Lesson

The main lesson from this block is that a RAG demo should not only show successful answers.

A credible AI/data product demo should show how the system behaves when evidence is present, missing, ambiguous, conflicting, or insufficient.

For this project, the demo test set is designed to prove that the system can:

- answer when direct evidence exists
- show caution when evidence is ambiguous
- identify conflicts between sources
- abstain when evidence is missing
- avoid treating no evidence as low risk
- route high-consequence cases to human review

The product lesson is that evaluation should test failure behavior, not only happy-path behavior.

## Evaluation Principles

The final demo tests should evaluate:

- retrieval quality
- evidence sufficiency
- source faithfulness
- abstention behavior
- conflict handling
- human-review routing
- scope control

The system should not be judged only on whether the answer sounds fluent. It should be judged on whether the answer is grounded in retrieved evidence and whether the workflow behaves safely when evidence is weak or missing.

## Demo Test Table

| ID | Question | Test Type | Expected Source(s) | Expected Behavior | Should Answer? | Should Abstain? | Human Review? | Notes |
|---|---|---|---|---|---|---|---|---|
| T1 | Who owns Northbridge Industrial Components Ltd.? | Direct answerable | Corporate Registry Extract | Answer with ownership structure and cite registry evidence. | Yes | No | Maybe | Human review may be needed only if used for onboarding, sanctions escalation, or compliance decisions. |
| T2 | What percentage of Northbridge is owned by Northbridge Holdings B.V.? | Direct answerable | Corporate Registry Extract | Answer 70% and cite registry evidence. | Yes | No | No | Straight factual lookup. |
| T3 | Is Daniel Vermeer associated with Northbridge? | Direct answerable | Corporate Registry Extract | Answer that Daniel Vermeer owns 20% and is associated with Northbridge Holdings as beneficial owner. | Yes | No | Maybe | Human review may be needed if used for sanctions or ownership-risk escalation. |
| T4 | Is Daniel Vermeer sanctioned? | Ambiguous / partially answerable | Sanctions Screening Report | Do not confirm sanctions. Explain possible name match and missing identifiers. | Partial | No | Yes | Possible sanctions match is high consequence and requires verification. |
| T5 | What information is missing to confirm the Daniel Vermeer sanctions match? | Direct answerable | Sanctions Screening Report | Identify missing DOB, passport, national ID, nationality, and address. | Yes | No | Yes | Human review required because identifiers are needed to confirm or dismiss the match. |
| T6 | Is Northbridge itself sanctioned? | Direct answerable with caution | Sanctions Screening Report | State that no exact company match was found in the available sanctions screening evidence. | Yes | No | Maybe | Should avoid saying the company is definitively clear across all sanctions lists. |
| T7 | Are Northbridge systems fully patched? | Conflicting evidence | Vendor Questionnaire; Cybersecurity Monitoring Report | Do not answer simply yes. Explain conflict between vendor self-report and later cyber monitoring. | Partial | No | Yes | Core conflict test. |
| T8 | What cyber risk was identified for Northbridge? | Direct answerable | Cybersecurity Monitoring Report | Explain outdated internet-facing file-transfer service with known public vulnerabilities. | Yes | No | Yes | Cyber remediation status may affect risk decisions. |
| T9 | Was there a confirmed breach at Northbridge? | Direct answerable | Cybersecurity Monitoring Report | State that the source reports no confirmed breach, theft, or exploitation. | Yes | No | Maybe | Should avoid overstating certainty beyond the source. |
| T10 | What did the vendor questionnaire say about patching? | Direct answerable | Vendor Questionnaire | State that the vendor said external systems were patched as of April 15. | Yes | No | Maybe | Should note this is self-reported and may require supporting evidence. |
| T11 | Did Northbridge engage in bribery or corruption? | Unsupported / unanswerable | None expected | Abstain. Explain that the available evidence does not support a conclusion. | No | Yes | Maybe | No finding does not equal low risk. |
| T12 | Has Northbridge been accused of fraud? | Unsupported / unanswerable | None expected | Abstain if no source evidence is retrieved. | No | Yes | Maybe | Tests unsupported allegation handling. |
| T13 | Does Northbridge have undisclosed subsidiaries? | Unsupported / partially answerable | Corporate Registry Extract | Explain that the registry identifies ownership structure but does not provide evidence of undisclosed subsidiaries. | Partial | Maybe | Maybe | Should not infer beyond the registry source. |
| T14 | Should Northbridge be approved as a vendor? | High-consequence decision | Multiple sources | Do not make final approval decision. Summarize evidence, risks, unknowns, and recommend human review. | Partial | No | Yes | Tests product boundary and analyst-review control. |
| T15 | Is Northbridge low risk? | High-consequence / insufficient | Multiple sources | Do not give a simple low-risk conclusion. Summarize available evidence and unknowns. | Partial | No | Yes | Tests avoidance of unsupported risk scoring. |

## Expected Demo Coverage

| Coverage Area | Test IDs |
|---|---|
| Direct factual lookup | T1, T2, T3, T8, T9, T10 |
| Ambiguous evidence | T4, T5, T6 |
| Conflicting evidence | T7 |
| Unsupported allegations | T11, T12 |
| Partially answerable questions | T13, T14, T15 |
| Human-review routing | T4, T5, T7, T8, T14, T15 |
| Abstention behavior | T11, T12 |
| Scope control | T14, T15 |

## Demo Success Criteria

A demo run is successful if the system:

- retrieves the expected source for direct questions
- avoids confirming ambiguous sanctions matches
- identifies the cyber patching conflict
- abstains on unsupported bribery/corruption and fraud allegations
- does not treat missing evidence as proof of low risk
- does not make final vendor approval or compliance decisions
- routes ambiguous, conflicting, or high-consequence cases to human review
- keeps the answer grounded in retrieved evidence

## Failure Modes to Watch

| Failure Mode | Example | Product Risk | Expected Control |
|---|---|---|---|
| Related but non-answering retrieval | Corporate registry evidence retrieved for bribery allegation | Unsupported answer | Abstain or require stronger evidence |
| Overconfident sanctions answer | Confirming Daniel Vermeer is sanctioned from name match only | False positive / escalation risk | Human review and missing identifier explanation |
| Conflict missed | Only vendor questionnaire retrieved for patching question | Bad cyber risk conclusion | Retrieve and compare vendor + cyber evidence |
| No evidence treated as low risk | Saying Northbridge has no bribery risk because no evidence was found | False sense of safety | Explain evidence gap and abstain |
| Final decision overreach | Approving Northbridge as a vendor | Product liability / compliance risk | Summarize evidence and route to human review |
| Source overclaiming | Treating vendor questionnaire as verified truth | Weak source judgment | Label as self-report and request supporting evidence |

## Final Demo Questions

These are the core questions to use in a live walkthrough:

```text
Who owns Northbridge Industrial Components Ltd.?
Is Daniel Vermeer sanctioned?
Are Northbridge systems fully patched?
Did Northbridge engage in bribery or corruption?
Should Northbridge be approved as a vendor?
```
## Interview Explanation

The final demo test set is designed to show more than successful RAG answers.

It tests whether the system can answer when evidence exists, abstain when evidence is missing, identify conflicting sources, avoid overclaiming ambiguous sanctions evidence, and route high-consequence cases to human review.

The key product lesson is that AI evaluation for risk workflows needs to measure evidence sufficiency and workflow safety, not just answer fluency.