# Week 2 Evaluation Notes

## Controlled Context Versus RAG

The current implementation uses controlled-context grounding. The application reads one predetermined vendor case and sends the full source material to Claude with instructions to use only that evidence.

This differs from a basic LLM call because the model receives an approved source context and is instructed to identify evidence, uncertainty, and human-review needs.

It is not yet full retrieval-augmented generation. A RAG workflow would search a larger document collection, rank relevant passages, and send only the retrieved evidence to the model.

I chose to test controlled grounding first so that evidence use, abstention, traceability, and escalation behavior could be evaluated before adding retrieval complexity.

## Evaluation Summary

| Test | Expected behavior | Actual behavior | Result | Product implication |
|---|---|---|---|---|
| Supported evidence | Identify supported risks with source references and appropriate uncertainty | [Complete after reviewing output] | Pass / Partial / Fail | Determines whether the model can create a reviewable risk summary from supplied evidence | | Insufficient evidence | Abstain and avoid unsupported allegations | [Complete after reviewing output] | Pass / Partial / Fail | Tests whether the workflow reduces hallucination and reputational risk | | Conflicting evidence | Surface the contradiction without choosing a source | [Complete after reviewing output] | Pass / Partial / Fail | Tests whether the workflow preserves uncertainty and supports escalation |

## Initial Findings

### What Worked

- [Example: The model consistently referenced supplied source labels.]
- [Example: It distinguished a potential sanctions match from a confirmed match.]
- [Example: It surfaced the cybersecurity conflict.]

### What Did Not Work Reliably

- [Record any vague source references.]
- [Record any unsupported statement.]
- [Record any inconsistent confidence level.]
- [Record whether “human review required” was too broad or too weak.]

### Product Implications

A working API response is not sufficient evidence of product quality. The workflow must be tested against supported, unsupported, and conflicting scenarios.

The initial tests provide a baseline, but three examples are not enough to establish production reliability. Future evaluation should include a larger set of questions, explicit scoring criteria, repeated runs, and retrieval-specific failure cases.

## Quality Concepts

**Groundedness:** Material claims should be supported by the supplied source evidence.

**Abstention:** When the evidence does not answer the question, the model should state that evidence is insufficient rather than infer or invent a conclusion.

**Traceability:** Important findings should reference the source labels that support them.

**Human review:** Review should be recommended when evidence is missing, conflicting, identity-sensitive, or materially consequential.