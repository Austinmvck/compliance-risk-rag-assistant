# Human-Review Decision Table

## Purpose

This document defines when the Compliance Risk RAG Assistant should answer, abstain, or route a case to human review.

The assistant is designed to support compliance and third-party risk workflows. It should not independently make final compliance decisions, confirm sanctions status, validate allegations, or replace analyst review.

Human review is required when the evidence is ambiguous, conflicting, stale, low-confidence, unsupported, or consequential enough that an automated answer could create false confidence.

## Decision Table

| Trigger condition | Evidence signal | System behavior | Human action | Owner |
|---|---|---|---|---|
| Possible sanctions name match | Sanctions source shows a possible match for Daniel Vermeer, but key identifiers such as date of birth, passport number, national ID, nationality, or residential address are missing. | Do not confirm sanctioned status. State that the match is possible but unverified. Route to human review. | Verify identifiers against authoritative sanctions sources and internal screening procedures. | Compliance Analyst |
| No exact sanctions match for company | Sanctions screening says there is no exact sanctions match for Northbridge Industrial Components Ltd. | State that no exact company match was found in the retrieved source. Do not extend this conclusion to all related parties or beneficial owners. | Review related entities, beneficial owners, and updated watchlist results if the decision is high-risk. | Compliance Analyst |
| Unsupported bribery/corruption allegation | User asks whether Northbridge engaged in bribery or corruption, but no relevant enforcement, adverse media, legal, or anti-bribery source is retrieved above threshold. | Abstain before generation. State that no relevant evidence was retrieved and that the allegation is unsupported by the current corpus. | Gather targeted sources such as enforcement databases, adverse media, litigation records, and anti-bribery/corruption disclosures. | Risk Analyst |
| Conflicting cyber evidence | Vendor questionnaire states external systems were patched, but cyber monitoring identifies outdated software on an internet-facing file-transfer service after the questionnaire date. | Surface the conflict. Do not decide which source is correct. Recommend verification and human review. | Request remediation evidence, scan results, patch dates, and confirmation from security or vendor risk teams. | Vendor Risk Analyst / Security Analyst |
| Vendor self-report without supporting evidence | Vendor questionnaire makes a control or remediation claim but does not include supporting scan, audit, remediation, or validation evidence. | Treat the claim as self-reported. Do not present it as independently verified. | Request supporting evidence or independent validation. | Vendor Risk Analyst |
| Cyber vulnerability without confirmed breach | Cyber monitoring identifies outdated software or known vulnerabilities but does not confirm exploitation, data theft, or breach. | Report the vulnerability finding. Do not claim breach, exploitation, or data compromise. Route if risk severity or exposure is material. | Validate exploitability, exposure, remediation status, and incident history. | Security Analyst |
| Low retrieval confidence | Retrieved chunks fall below the minimum similarity threshold or no chunks are retrieved. | Abstain before generation. State that no relevant evidence was retrieved above threshold. | Gather additional sources or reformulate the research question. | Analyst / Product Workflow |
| Topically related but non-answering evidence | Retrieved chunks are broadly compliance-related but do not directly support, contradict, or answer the user’s question. | Avoid treating adjacent context as evidence. State the limitation and route to review if the question is consequential. | Determine whether additional source types are needed. | Risk Analyst |
| Stale source date | Retrieved source is materially older than another source or older than the decision window. | Flag source freshness. Avoid treating stale evidence as current unless confirmed by newer data. | Refresh source data or compare against newer authoritative records. | Data Operations / Analyst |
| Ownership ambiguity | Corporate registry identifies shareholders but does not provide full ownership of parent companies or private investors. | State known ownership facts and explicitly identify ownership gaps. Do not infer parent ownership beyond the source. | Conduct beneficial ownership review and request additional registry or UBO sources. | Compliance Analyst |
| Conflicting source types | Vendor self-attestation conflicts with external monitoring, registry data, sanctions screening, adverse media, or other independent sources. | Present both sources with dates and source types. Do not resolve the conflict automatically. | Review source reliability, freshness, and supporting documentation before decisioning. | Compliance Analyst / Risk Analyst |
| High-consequence decision | The answer could affect onboarding, renewal, escalation, sanctions screening, vendor approval, or customer-facing risk reporting. | Require human review even if the answer appears grounded. | Review evidence, confidence, source authority, and business impact before action. | Compliance / Product / Risk Owner |

## Product Rules

1. The assistant should support analyst judgment, not replace it.
2. Missing evidence should not be treated as evidence of no risk.
3. Possible sanctions matches should never be converted into confirmed matches without identifier validation.
4. Vendor self-reports should not be treated as independently verified evidence.
5. Cyber vulnerability findings should not be inflated into confirmed breaches.
6. Conflicting evidence should be surfaced, not automatically resolved.
7. Low retrieval confidence should trigger abstention before generation.
8. Source type, source date, and source authority should influence routing and review priority.

## Product Lesson

Human-in-the-loop design is not just adding a human reviewer at the end of an AI workflow.

A useful compliance AI workflow needs explicit rules for when the system should answer, abstain, escalate, or request more evidence. The human-review table converts uncertainty into an operational workflow by defining the trigger condition, evidence signal, system behavior, human action, and owner.

This is especially important in third-party risk and compliance workflows because false positives, false negatives, stale sources, unsupported allegations, and conflicting evidence can all create downstream decision risk.

## Observational Notes for Key Human-Review Rows

### 1. Possible sanctions name match

This row exists because a name-only sanctions match can create a false positive. A person may share the same or similar name as a listed individual without being the same person.

The trigger is a sanctions source showing a possible match for Daniel Vermeer while missing identity-confirming fields such as date of birth, passport number, national ID, nationality, or residential address.

The system should not confirm sanctioned status. It should state that the match is possible but unverified, identify the missing identifiers, and route the case to human review.

The human analyst should verify the identity against authoritative sanctions sources and internal screening procedures. The system should not make the final identity-match decision.

This connects to my AI/data and supply chain risk management experience because third-party risk workflows often surface possible risk matches from multiple sources, but a possible match must be adjudicated before it is treated as confirmed risk.

---

### 2. Unsupported bribery/corruption allegation

This row exists because bribery and corruption allegations are consequential and should not be inferred from adjacent risk data. A lack of retrieved evidence does not prove low risk; it only means the current corpus does not support the allegation.

The trigger is a user asking whether Northbridge engaged in bribery or corruption when no enforcement, adverse media, litigation, legal proceeding, or anti-bribery/corruption source is retrieved above threshold.

The system should abstain before generation and state that no relevant evidence was retrieved from the current corpus. It should not imply that Northbridge is cleared of bribery or corruption risk.

The human analyst should gather targeted sources such as adverse media, enforcement databases, litigation records, regulatory disclosures, and anti-bribery/corruption records before making a judgment.

This connects to my AI/data and supply chain risk management experience because risk products need to distinguish between “no evidence found in current sources” and “risk does not exist.” Those are different conclusions.

---

### 3. Conflicting cyber evidence

This row exists because vendor-provided evidence and external monitoring evidence can point in different directions. The system should identify the conflict but should not decide which source reflects the current truth.

The trigger is the vendor questionnaire stating that external systems were patched while a later cybersecurity monitoring report identifies outdated software on an internet-facing file-transfer service.

The system should surface both sources, show their dates and source types, and state that the evidence conflicts. It should not resolve the conflict automatically.

The human analyst should request updated documentation, scan results, patch dates, remediation evidence, and confirmation from security or vendor risk teams.

This connects to my AI/data and supply chain risk management experience because third-party risk workflows often involve conflicting source data. The product needs a review path for reconciling source disagreement before the evidence is used for a business, vendor, or compliance decision.

---

### 4. Vendor self-report without supporting evidence

This row exists because a vendor claim is not the same as independent verification. A questionnaire response can be useful, but it should not be treated as proven if no supporting evidence is attached.

The trigger is a vendor questionnaire making a control, patching, or remediation claim without supporting scan results, audit evidence, remediation records, or independent validation.

The system should acknowledge the vendor claim but label it as self-reported. It should not present the claim as independently verified.

The human analyst should request supporting evidence from the vendor or obtain independent validation from security, audit, monitoring, or data quality sources.

This connects to my AI/data and supply chain risk management experience because customer-facing risk products need to avoid overstating confidence. Presenting unverified claims as verified evidence can create downstream business and compliance risk.

---

### 5. Topically related but non-answering evidence

This row exists because retrieved evidence can be related to the general compliance topic without actually answering the user’s question. This became visible during semantic retrieval testing, where the bribery/corruption question retrieved compliance-adjacent chunks that did not support the allegation.

The trigger is a retrieval result that is broadly compliance-related but does not directly support, contradict, or answer the question being asked.

The system should avoid treating adjacent context as evidence. It should state the limitation, abstain if necessary, and route to review when the question is consequential.

The human analyst should determine whether the correct source type is missing and whether additional research is needed.

This connects to my AI/data and supply chain risk management experience because risk systems often retrieve or display evidence that still requires adjudication. A human reviewer may need to decide whether the evidence actually answers the risk question or is merely related background.
