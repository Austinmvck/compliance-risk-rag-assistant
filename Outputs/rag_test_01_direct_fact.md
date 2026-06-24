# RAG Test 01 — Direct Fact Retrieval

## Test Purpose

Determine whether the RAG workflow can retrieve the correct source evidence and answer a direct ownership question without adding unsupported details.

## Question

Who owns Northbridge Industrial Components Ltd.?

## Expected Behavior

- Retrieve Corporate Registry evidence.
- Summarize ownership percentages accurately.
- Reference source name and chunk IDs.
- Avoid unsupported parent-company ownership claims.
- Identify missing ownership details if evidence is incomplete.

## Retrieved Evidence

================================================================================
Rank: 1
Similarity score: 0.3629
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
Similarity score: 0.1021
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
According to the Corporate Registry Extract from the Netherlands, Northbridge Industrial Components Ltd. has the following ownership structure:
- Northbridge Holdings B.V. owns 70% of the company
- Daniel Vermeer owns 20% of the company
- Private investors own 10% of the company

Additionally, Daniel Vermeer is identified as a beneficial owner associated with Northbridge Holdings B.V., suggesting he may have indirect control beyond his direct 20% stake.

Evidence used:
The ownership information comes from a Dutch government corporate registry extract dated 2026-05-01, with registry information last updated on 2025-11-18.

Source references:
- SOURCE_A_CHUNK_1 (Corporate Registry Extract, similarity score: 0.3629)
- SOURCE_A_CHUNK_2 (Corporate Registry Extract, similarity score: 0.1021)

Unknowns or conflicting information:
- The registry does not provide information about who owns or controls Northbridge Holdings B.V. beyond Daniel Vermeer's association as a beneficial owner
- The specific identities of the "private investors" holding 10% are not disclosed
- The exact nature and extent of Daniel Vermeer's beneficial ownership in Northbridge Holdings B.V. is not detailed
- Ultimate beneficial ownership beyond the first ownership layer cannot be determined from the retrieved evidence

Confidence:
High confidence in the direct ownership percentages as stated in the government registry. Lower confidence in understanding the complete ownership chain and ultimate beneficial ownership.

Human review required:
Yes. To fully understand ownership and control, further investigation is needed into: (1) the ownership structure of Northbridge Holdings B.V., (2) the extent of Daniel Vermeer's beneficial ownership and control rights, and (3) the identity of the private investors holding 10%.

## Initial Assessment

Retrieval quality: Pass  
Answer groundedness: Pass  
Source references: Pass  
Unsupported claims: Partial/Pass  
Human review behavior: Pass

## Notes

The system retrieved the Corporate Registry chunks as the top evidence. One irrelevant zero-score cyber chunk was also retrieved, which shows the need for a future similarity threshold. Claude ignored the irrelevant chunk and answered from the Corporate Registry evidence. Another point out is the speculation that Daniel Vermeer could also own an additional 10% as the beneficial owner edges slightly towards assumption and think that could have been worded better.