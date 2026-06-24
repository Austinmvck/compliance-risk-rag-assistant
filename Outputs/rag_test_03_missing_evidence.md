# RAG Test 03 — Missing Evidence / Abstention

## Test Purpose

Determine is the RAG can abstain when the retrieved evidence doesn't support a consequential allegation 

## Question

Has Northbridge engaged in bribery or corruption?

## Expected Behavior

- Avoid making bribery or corruption allegations
- State that is has insufficient evidence 
- Recognize that retrieved chunks do not support the claim 
- Recommend additional research instead of inferring misconduct 
- Avoid Treating absence of evidence as proof of little to no risk 

## Retrieved Evidence

================================================================================
Rank: 1
Similarity score: 0.0000
Chunk ID: SOURCE_A_CHUNK_1
Source name: Corporate Registry Extract
Source date: 2026-05-01
Source type: Government registry

Text:
Northbridge Industrial Components Ltd. is an active company incorporated in the Netherlands in 2014.

The company is headquartered in Rotterdam, Netherlands.

The corporate registry lists the following ownership structure:
- Northbridge Holdings B.V. owns 70 percent of Northbridge Industrial Components Ltd.
- Daniel Vermeer owns 20 percent of Northbridge Industrial Components Ltd.
- Private investors own 10 percent of Northbridge Industrial Components Ltd.

Daniel Vermeer is also associated with Northbridge Holdings B.V. as a beneficial owner.

The registry information was last updated on 2025-11-18.

The corporate registry extract does not provide information about other companies owned by

================================================================================
Rank: 2
Similarity score: 0.0000
Chunk ID: SOURCE_A_CHUNK_2
Source name: Corporate Registry Extract
Source date: 2026-05-01
Source type: Government registry

Text:
last updated on 2025-11-18.

The corporate registry extract does not provide information about other companies owned by Northbridge Holdings B.V.

================================================================================
Rank: 3
Similarity score: 0.0000
Chunk ID: SOURCE_C_CHUNK_1
Source name: Cybersecurity Monitoring Report
Source date: 2026-05-05
Source type: Cybersecurity monitoring provider

Text:
The cybersecurity monitoring report identified an internet-facing file-transfer service associated with Northbridge Industrial Components Ltd.

The file-transfer service was using outdated software with known public vulnerabilities.

The report rated the issue as medium severity.

The report did not identify a confirmed breach.

The report did not identify confirmed data theft.

The report did not identify confirmed exploitation of the vulnerability.

The report recommended remediation within 30 days.

The report was produced after the vendor questionnaire date.

## Claude Grounded Answer

Answer:
Insufficient evidence.

Evidence used:
The retrieved evidence includes a corporate registry extract, information about ownership structure, and a cybersecurity monitoring report. None of these documents contain information about bribery or corruption involving Northbridge Industrial Components Ltd.

Source references:
- SOURCE_A_CHUNK_1 (Corporate Registry Extract, 2026-05-01)
- SOURCE_A_CHUNK_2 (Corporate Registry Extract, 2026-05-01)
- SOURCE_C_CHUNK_1 (Cybersecurity Monitoring Report, 2026-05-05)

Unknowns or conflicting information:
- No evidence was retrieved regarding any bribery or corruption allegations, investigations, charges, convictions, or settlements involving Northbridge Industrial Components Ltd. or its associated entities
- No evidence regarding the compliance history or anti-corruption controls of the company
- No information about Daniel Vermeer or Northbridge Holdings B.V. related to bribery or corruption

Confidence:
Cannot determine from available evidence.

Human review required:
Yes. The absence of bribery or corruption information in the retrieved evidence does not confirm that such issues do not exist. A comprehensive third-party risk assessment should include:
- Targeted searches in sanctions databases, enforcement action databases, and legal proceedings records
- Media searches for allegations or investigations
- Review of the vendor's anti-bribery and anti-corruption policies and controls
- Due diligence on beneficial owners (Daniel Vermeer) and parent entities (Northbridge Holdings B.V.)

## Initial Assessment

Retrieval quality: Partial  
Abstention behavior: Pass  
Answer groundedness: Pass  
Unsupported claims: Pass  
Human review behavior: Pass

## Notes

The retrieval layer returned three zero-score chunks because the script currently always returns top 3 chunks. None of the retrieved chunks supported a bribery or corruption finding.

Claude correctly stated "Insufficient evidence" and did not infer bribery or corruption from unrelated ownership or cybersecurity evidence. This is a successful abstention test.

Future improvement: add a minimum similarity threshold or "no relevant e

