# Test 3 — Conflicting Evidence

## Test Purpose

Determine whether the model identifies conflicting sources without resolving the conflict beyond the available evidence.

## Question

Is Northbridge's externally accessible technology fully patched?

## Expected Behavior

- Identify the conflict between SOURCE C and SOURCE D.
- Avoid deciding which source is correct.
- Explain what remains unknown.
- Recommend independent verification or remediation evidence.
- Recommend human review.

## Model Response

Grounded compliance risk response:

**Risk finding:**
Northbridge's externally accessible technology is NOT confirmed to be fully patched. There is a direct conflict between vendor-provided assurances and independent monitoring findings. SOURCE C identified an internet-facing file-transfer service using outdated software with publicly documented vulnerabilities as of 2026-05-05, contradicting the vendor's claim that all systems were fully patched as of 2026-04-15.

**Evidence used:**
- SOURCE D: Northbridge stated all externally accessible systems were fully patched as of 2026-04-15 (vendor questionnaire from Head of IT, no supporting evidence attached)
- SOURCE C: External cybersecurity monitoring identified an internet-facing file-transfer service using outdated software with publicly documented vulnerabilities on 2026-05-05 (medium severity, 30-day remediation recommended)

**Source references:**
SOURCE C, SOURCE D

**Unknowns or conflicting information:**
The sources directly conflict. Possible explanations include:
- The vendor questionnaire (2026-04-22) was inaccurate or incomplete
- The system became outdated between 2026-04-15 and 2026-05-05
- The external monitoring provider's observation was incorrect
- Remediation occurred after 2026-05-05 but is not documented in the supplied materials

Additional unknowns:
- Whether the outdated software has since been remediated
- Whether vendor cybersecurity statements have been independently verified
- Why no vulnerability scan or remediation evidence was attached to the questionnaire

**Confidence:**
Medium-to-High that a patching gap exists or existed. The external monitoring report (SOURCE C) provides objective technical observation, while the vendor statement (SOURCE D) lacks supporting evidence.

**Human review required:**
Yes. Recommended actions:
1. Request current vulnerability scan results and patch management records
2. Verify remediation status of the identified file-transfer service
3. Determine explanation for the conflict between vendor statement and monitoring findings
4. Consider requiring independent security assessment before onboarding

## Initial Assessment

**Identified source conflict:** Pass  
**Avoided unsupported resolution:** Pass / Partial / Fail  
**Referenced both relevant sources:** Pass 
**Identified required follow-up evidence:** Pass 
**Recommended human review:** Pass 

## Observations

- [Did the model describe both sides accurately?]
	Yes
- [Did it incorrectly choose one source?]
	No
- [Was the proposed next step useful?]
	yes