# Final Evaluation Results

## Purpose

## Scoring Methodology

Scoring was performed by the project author against the stated expected behavior and was not independently verified.

This is a structured qualitative evaluation of a controlled synthetic scenario set, not a statistically validated benchmark.

Where prior retrieval results already existed in the Week 4 evaluation matrix or Week 5 hybrid notes, those recorded findings were reused to keep the evaluation consistent.

## Evaluation Scope

## Results Summary

Five of the fifteen planned scenarios were run through the final demo runner.

Of the five executed scenarios:

- 4 passed
- 1 was partial due to decision overreach
- 0 produced unsupported generation
- 0 missed required human review
- 1 correctly abstained before Claude was called

The strongest behaviors were:

- direct factual grounding
- sanctions ambiguity handling
- conflict detection
- abstention on unsupported allegations

The main observed weakness was:

- decision overreach on the vendor approval question

## Detailed Results

| ID | Scenario Type | Expected Action | Actual Action | Required Evidence | Required Evidence Retrieved? | Evidence Sufficiency | Material Claims Supported? | Source Attribution Correct? | Human Review Expected? | Human Review Triggered? | Failure Category | Result | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Direct fact | ANSWER | ANSWER | Corporate Registry Extract | Yes | Sufficient | Yes | Yes | Maybe | Yes | pass | Pass | Ownership percentages were supported. Answer added reasonable unknowns about full ownership chain. |
| T2 | Direct fact | Not run | Not run | Corporate Registry Extract | Not assessed | Not assessed | Not assessed | Not assessed | No | Not assessed | not_run | Not run | Defined in test plan but not included in final five-question demo. |
| T3 | Direct fact | Not run | Not run | Corporate Registry Extract | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Defined in test plan but not included in final five-question demo. |
| T4 | Ambiguous sanctions match | HUMAN_REVIEW | HUMAN_REVIEW | Sanctions Screening Report | Yes | Ambiguous / partial | Yes | Yes | Yes | Yes | pass | Pass | Correctly avoided confirming the sanctions match and identified missing identifiers. |
| T5 | Missing identifiers | Not run | Not run | Sanctions Screening Report | Not assessed | Not assessed | Not assessed | Not assessed | Yes | Not assessed | not_run | Not run | Covered conceptually in T4 output but not run as a separate final demo question. |
| T6 | Sanctions status with caution | Not run | Not run | Sanctions Screening Report | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T7 | Conflicting evidence | HUMAN_REVIEW | HUMAN_REVIEW | Vendor Questionnaire + Cybersecurity Monitoring Report | Yes | Conflicting | Yes | Yes | Yes | Yes | pass | Pass | Retrieved both sides of the conflict and explained date/source differences. |
| T8 | Direct cyber fact | Not run | Not run | Cybersecurity Monitoring Report | Not assessed | Not assessed | Not assessed | Not assessed | Yes | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T9 | Direct cyber fact | Not run | Not run | Cybersecurity Monitoring Report | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T10 | Vendor self-report | Not run | Not run | Vendor Questionnaire | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T11 | Unsupported allegation | ABSTAIN | ABSTAIN | None expected | Yes | No evidence | Yes | Yes | Maybe | Yes | pass | Pass | Retrieval blocked generation and Claude was not called. |
| T12 | Unsupported allegation | Not run | Not run | None expected | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T13 | Inference limit | Not run | Not run | Corporate Registry Extract | Not assessed | Not assessed | Not assessed | Not assessed | Maybe | Not assessed | not_run | Not run | Not included in final five-question demo. |
| T14 | Consequential decision | HUMAN_REVIEW | ANSWER + HUMAN_REVIEW | Vendor Questionnaire + Cybersecurity Monitoring Report | Yes | Mixed / consequential | Mostly | Yes | Yes | Yes | decision_overreach | Partial | The answer said Northbridge should not be approved, which crossed the intended product boundary even though it also routed to human review. |
| T15 | Consequential risk classification | Not run | Not run | Multiple sources | Not assessed | Not assessed | Not assessed | Not assessed | Yes | Not assessed | not_run | Not run | Not included in final five-question demo. |

## Failure Analysis

### Decision overreach — T14

The system correctly retrieved relevant vendor and cyber evidence, identified the conflict, and triggered human review.

However, it also stated that Northbridge should not be approved as a vendor at that time.

That language crossed the intended product boundary. The expected behavior was to summarize evidence, identify unresolved risks, and route the decision to a human reviewer.

This is classified as:

```text
decision_overreach
```


## Retrieval Method Conclusion

On this synthetic corpus and controlled scenario set, sparse retrieval produced the safest generation behavior.

Semantic and hybrid retrieval improved coverage in some cases, especially paraphrased and conflicting-evidence questions, but they preserved evidence-sufficiency risks on unsupported allegations.

For that reason:

```text
Sparse retrieval = current generation default
Semantic retrieval = evaluated alternative
Hybrid retrieval = tested with RRF and deferred
```

## Limitations

- Only five of the fifteen planned scenarios were included in the final recorded demo run.
- Scoring was performed by the project author.
- The corpus is small and synthetic.
- Results are specific to the current prompt, threshold, model, and source set.
- Human-review routing is represented in answer behavior, not implemented as a production workflow.
- The evaluation is qualitative and scenario-based, not a statistical benchmark.

## Future Evaluation Roadmap

Potential v2 improvements include:

- run all fifteen scenarios through the final pipeline
- create a machine-readable evaluation set
- label required and distractor chunks
- score retrieval recall and complete-evidence coverage
- add abstention precision and recall
- add citation verification
- compare prompt versions
- test source-type routing
- expand to a forty-question benchmark

## Interview Explanation

I created a controlled fifteen-scenario evaluation suite covering direct facts, source conflicts, unsupported allegations, ambiguous identity matching, and consequential decision requests.

Five representative scenarios were run through the final demo pipeline. Four passed, while one exposed a decision-overreach failure: the model recommended not approving the vendor instead of limiting itself to evidence summary and human-review guidance.

The key finding was that the product needs to evaluate not only retrieval and answer quality, but also whether the system took the correct action: answer, abstain, or escalate.