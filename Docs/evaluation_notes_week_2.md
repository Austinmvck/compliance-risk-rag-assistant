# Week 2 Evaluation Notes

## Controlled Context Versus RAG

The current implementation uses controlled-context grounding. The application reads one predetermined vendor case and sends the full source material to Claude with instructions to use only that evidence.

This differs from a basic LLM call because the model receives an approved source context and is instructed to identify evidence, uncertainty, and human-review needs.

It is not yet full retrieval-augmented generation. A RAG workflow would search a larger document collection, rank relevant passages, and send only the retrieved evidence to the model.

I chose to test controlled grounding first so that evidence use, abstention, traceability, and escalation behavior could be evaluated before adding retrieval complexity.

## Evaluation Summary

## Evaluation Summary

| Test | Expected behavior | Actual behavior | Result | Product implications |
|---|---|---|---|---|
| Supported evidence | Will identify supported compliance risks, will reference the supplied sources, it will distinguish confirmed facts from unresolved risks, acknowledge uncertainty levels and confidence, and recommend human review. | The model identified possible sanctions-name match, while clearly stated that it was unconfirmed, referenced the supplied source labels, stated material unknowns and confidence levels, and recommended targeted human-review actions. | Pass | Controlled grounding could produce a structured, reviewable risk summary when the relevant evidence is supplied and explicit. This concluded that the model could use approved context before retrieval complexity is introduced. |
| Insufficient evidence | Explicitly state that the available evidence is insufficient, avoid making and implying an unsupported bribery or corruption allegation, explain that the supplied sources do not answer the question, and recommend further research without making judgment. | The model explicitly stated that there was insufficient evidence, avoided unsupported allegations, Explain that none of the supplied sources addressed bribery or corruption, identified missing information, and recommended additional diligence. The follow-up actions are directionally appropriate realative to the asked question | Pass | Controlled grounding reduced unsupported generation and showed that the model could abstain when the evidence did not support a conclusion. The test also showed that escalation guidance should remain in relation to the specific question. |
| Conflicting evidence | Identify the conflict between the vendor questionnaire and external cyber-monitoring report, accurately describe both sources, avoid deciding which source is correct, explain what remains unknown, request independent verification or remediation evidence, and recommend human review. | The model identified and accurately represented both conflicting sources, stated that the technology was not confirmed to be fully patched, maintianed uncertainty about why the sources differed, described possible explanations, identified the missing remediation evidence, and recommended independent verification and human review. | Pass | Controlled grounding handled conflicting evidence effectively when both sides were explicitly included in the context. The result supported moving to retrieval testing, where the next challenge was whether the system could reliably find all required conflicting evidence on its own. |

## Initial Findings

### What Worked

- Did a good job abstaining from unsupported evidence claims
- Identified conflicts with good accuracy
- Model did of great job in the traceability of the data it considered evidence

### What Did Not Work Reliably

- Didnt test measure the retrival quality since all evidence was supplied dirrectly
- Small cases which present huge limitations and what you can actually observe
- Confidence levels doesnt have a scale to measure on what is sufficent enough

### Product Implications

A working API response is not sufficient evidence of product quality. The workflow must be tested against supported, unsupported, and conflicting scenarios.

The initial tests provide a baseline, but three examples are not enough to establish production reliability. Future evaluation should include a larger set of questions, explicit scoring criteria, repeated runs, and retrieval-specific failure cases.

## Quality Concepts

**Groundedness:** Material claims should be supported by the supplied source evidence.

**Abstention:** When the evidence does not answer the question, the model should state that evidence is insufficient rather than infer or invent a conclusion.

**Traceability:** Important findings should reference the source labels that support them.

**Human review:** Review should be recommended when evidence is missing, conflicting, identity-sensitive, or materially consequential.
