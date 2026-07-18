# Week 5 Hybrid Retrieval Experiment

## Purpose

This experiment tested whether hybrid retrieval could improve the Compliance Risk RAG Assistant’s evidence-retrieval behavior.

By the end of Week 4, the system had three important findings:

1. Sparse retrieval performed well on abstention and conflict cases, especially when query expansion mapped user language to source terminology.
2. Semantic retrieval improved meaning-based matching, but it also returned related-but-non-answering chunks for unsupported allegations.
3. Semantic threshold tuning showed a recall-versus-precision tradeoff: higher thresholds improved abstention but risked filtering out evidence needed for conflict detection.

Hybrid retrieval was tested to determine whether combining sparse and semantic retrieval could improve evidence coverage without weakening abstention behavior.

The goal was not to assume that hybrid retrieval would be superior. The goal was to evaluate whether it produced safer and more complete evidence packages for the tested third-party risk workflow.

## Experiment Question

```text
Can sparse and semantic retrieval be combined in a way that improves evidence coverage while preserving evidence sufficiency and safe abstention?
```

## Method

The experiment used Reciprocal Rank Fusion, or RRF, to combine ranked sparse and semantic retrieval results.

RRF was chosen instead of raw score averaging because sparse-retrieval scores and semantic-embedding scores are not directly comparable.

Sparse retrieval scores are based on keyword or term overlap.

Semantic retrieval scores are based on embedding cosine similarity.

Because the scores exist on different scales, directly averaging them would create a misleading combined score.

RRF combines the ranked outputs rather than the raw similarity values.

```text
RRF score = 1 / (k + sparse rank) + 1 / (k + semantic rank)
```

The implementation used:

```text
RRF constant k = 60
Semantic minimum similarity threshold = 0.20
Maximum returned results = 5
```

Rank positions began at 1.

A chunk appearing in both retrieval lists received contributions from both methods and therefore tended to rank higher in the fused result.

A chunk appearing in only one list still remained eligible for the hybrid result, but received only one rank contribution.

## Implementation

The experiment was implemented in:

```text
Scripts/07_hybrid_retrieve_chunks.py
```

The script:

1. Loads the processed source chunks.
2. Runs the existing sparse retriever.
3. Runs semantic retrieval using `sentence-transformers/all-MiniLM-L6-v2`.
4. Applies the semantic threshold.
5. Combines the two ranked lists using Reciprocal Rank Fusion.
6. Returns the top fused results.
7. Prints:
   - chunk metadata
   - original sparse rank and score
   - original semantic rank and score
   - final RRF score
   - source text

The script is experimental and does not send evidence to Claude.

The active generation path remained:

```text
Sparse retrieval
→ minimum similarity threshold
→ Claude grounded answer or abstention
```

This separation was intentional so that the hybrid method could be evaluated before affecting answer generation.

## Why Reciprocal Rank Fusion Was Appropriate

RRF offered several advantages for this experiment:

- It avoided treating sparse and semantic scores as equivalent.
- It rewarded chunks retrieved highly by both methods.
- It preserved chunks found strongly by only one method.
- It remained simple enough to inspect and explain.
- It supported retrieval comparison without requiring a learned reranker.
- It reduced implementation complexity for a scoped product experiment.

RRF does not determine whether retrieved evidence is sufficient to answer the question.

It only combines retrieval rankings.

That distinction became central to the findings.

## Test Cases

The hybrid retriever was evaluated on representative question types covering:

| Test type | Example question | Evaluation focus |
|---|---|---|
| Direct fact | Who owns Northbridge Industrial Components Ltd.? | Whether hybrid retrieval preserved strong direct-fact performance |
| Sanctions ambiguity | Is Daniel Vermeer sanctioned? | Whether the sanctions report and identifying context were retrieved |
| Cyber risk | What cybersecurity risk was identified for Northbridge? | Whether the external monitoring evidence ranked highly |
| Conflicting evidence | Are Northbridge’s externally accessible systems fully patched? | Whether both the vendor questionnaire and later cyber report were surfaced |
| Unsupported allegation | Did Northbridge engage in bribery or corruption? | Whether hybrid retrieval incorrectly surfaced related-but-non-answering evidence |

These cases were selected because they represented distinct product risks:

- missing a direct fact
- missing an identity-sensitive source
- failing to retrieve both sides of a conflict
- returning evidence related to the domain but insufficient for the requested claim

## Evaluation Criteria

The experiment assessed:

- whether the required source appeared
- whether all required conflicting sources appeared
- whether unrelated or non-answering chunks appeared
- whether the result set improved evidence coverage
- whether retrieval behavior supported safe abstention
- whether the fused ranking was easier or harder to interpret
- whether the improvement justified changing the generation path

## Results Summary

| Test type | Sparse retrieval | Semantic retrieval | Hybrid retrieval | Assessment |
|---|---|---|---|---|
| Direct fact | Retrieved the expected registry evidence | Retrieved semantically relevant registry evidence | Preserved the expected source near the top | Pass |
| Sanctions ambiguity | Retrieved sanctions evidence through term overlap and query expansion | Retrieved the sanctions evidence through meaning similarity | Preserved the sanctions evidence and supporting context | Pass |
| Cyber risk | Retrieved the external monitoring report | Retrieved the relevant cyber evidence | Preserved strong cyber-risk coverage | Pass |
| Conflicting evidence | Retrieved the relevant conflict evidence and behaved safely | Improved meaning-based matching but threshold sensitivity affected complete conflict coverage | Surfaced both the vendor questionnaire and later monitoring report, improving conflict coverage | Pass |
| Unsupported allegation | Returned no usable evidence after sparse thresholding | Returned compliance-adjacent but non-answering evidence | Preserved related-but-non-answering chunks from the semantic side | Partial |

## Key Finding 1 — Hybrid Retrieval Improved Conflict Coverage

The strongest improvement occurred in the patching-conflict question.

The question required two sources:

- the vendor questionnaire stating that externally accessible systems were fully patched as of April 15
- the later cybersecurity monitoring report identifying outdated internet-facing software on May 5

Hybrid retrieval surfaced both sources in the fused evidence set.

This was useful because a one-sided result could have caused the answer to miss the contradiction entirely.

The experiment therefore showed that hybrid retrieval could improve multi-source evidence coverage in cases where different retrieval methods favored different wording or evidence types.

## Key Finding 2 — Hybrid Retrieval Did Not Solve Evidence Sufficiency

For the unsupported bribery or corruption question, semantic retrieval returned compliance-related chunks even though none answered the allegation.

Because RRF combines ranked results, those semantic results remained present in the hybrid output.

The retrieved chunks were related to:

- sanctions
- ownership
- compliance risk
- vendor evidence

But they did not establish:

- bribery
- corruption
- an investigation
- an allegation
- an enforcement action
- an admission

This exposed the main limitation of hybrid retrieval:

```text
More relevant-looking evidence does not necessarily mean sufficient evidence.
```

Hybrid retrieval improved coverage, but it could also preserve distractor evidence.

## Key Finding 3 — Ranking Agreement Was Useful but Not Decisive

Chunks retrieved highly by both sparse and semantic methods tended to rank strongly after fusion.

That provided a useful signal that both retrieval approaches considered the evidence relevant.

However, rank agreement did not prove that the chunk answered the user’s question.

A chunk could be:

- topically related
- highly ranked by both methods
- still insufficient to support the requested conclusion

RRF therefore improved ranking robustness but did not replace evidence-sufficiency evaluation.

## Key Finding 4 — Hybrid Retrieval Increased Inspection Complexity

Sparse retrieval was easier to inspect because the score could be traced to visible term overlap and query expansion.

Semantic retrieval required interpretation of embedding similarity.

Hybrid retrieval added another layer:

- sparse rank
- semantic rank
- sparse score
- semantic score
- fused RRF score

That additional complexity was acceptable for experimentation but increased the explanation and debugging burden.

For the current prototype, the benefit did not clearly outweigh the added complexity for the default generation path.

## Product Decision

Hybrid retrieval was not promoted to the default generation path.

The resulting decision was:

```text
Sparse retrieval = current generation default
Semantic retrieval = evaluated alternative
Hybrid retrieval = tested with Reciprocal Rank Fusion and deferred
```

The decision was based on observed behavior in the controlled corpus:

- hybrid retrieval improved conflict coverage
- hybrid retrieval preserved strong direct-evidence retrieval
- hybrid retrieval did not prevent related-but-non-answering evidence
- hybrid retrieval added interpretation and debugging complexity
- sparse retrieval continued to behave more safely on unsupported allegations

This is a scoped decision for the current prototype.

It does not prove that sparse retrieval is universally superior.

A larger corpus or different query distribution could justify a different retrieval architecture.

## Product Implications

### Retrieval coverage and evidence sufficiency are separate problems

A retrieval method can improve recall without improving answer safety.

The product must evaluate both:

```text
Did the system retrieve relevant evidence?
```

and:

```text
Is that evidence sufficient to support the requested claim?
```

### Hybrid retrieval may be more valuable for conflict-oriented queries

Questions requiring multiple differently worded sources may benefit from hybrid retrieval.

Examples include:

- vendor self-report versus external monitoring
- registry data versus sanctions evidence
- policy statement versus observed implementation
- earlier report versus later report

### Unsupported questions require stronger controls than ranking alone

No ranking method can guarantee abstention if topically related but non-answering evidence is still passed to the model.

Possible controls include:

- query-intent classification
- evidence-sufficiency scoring
- required-source rules
- entailment or claim-support checks
- negative-evidence detection
- post-retrieval policy checks
- stricter abstention logic

### Retrieval architecture should follow workflow risk

The safest method may differ by question type.

A future system could route:

- direct factual questions to sparse retrieval
- semantically phrased research questions to semantic retrieval
- conflict-detection questions to hybrid retrieval
- unsupported allegation questions through stricter evidence gates

This suggests that query-intent routing may ultimately be more useful than selecting one universal retriever.

## Limitations

The experiment had several limitations:

- The corpus was small and synthetic.
- The evaluation used a limited number of representative questions.
- Hybrid retrieval was evaluated at the retrieval layer only.
- Hybrid results were not passed through the full Claude generation workflow.
- The experiment did not measure latency or API cost.
- The experiment did not use repeated trials.
- No learned reranker was tested.
- No source-type weighting was implemented.
- No formal retrieval-recall or precision metric was calculated.
- The RRF constant was not tuned.
- The semantic threshold remained fixed at `0.20`.
- The findings may not generalize to larger or noisier corpora.

## Potential V2 Improvements

Potential follow-up experiments include:

- run the complete 15-scenario evaluation using hybrid retrieval
- compare sparse, semantic, and hybrid retrieval on identical required-evidence labels
- calculate required-source recall
- calculate distractor retrieval rate
- measure complete-evidence coverage for conflict questions
- test multiple semantic thresholds
- test different RRF constants
- add source-type weighting
- add query-intent routing
- add a reranking stage
- add evidence-sufficiency scoring
- test post-retrieval entailment checks
- measure latency and cost
- perform repeated runs and independent scoring

These are future maturity improvements, not requirements for the completed v1 prototype.

## Final Conclusion

The hybrid experiment demonstrated that combining sparse and semantic retrieval could improve evidence coverage, especially when a question required multiple conflicting sources.

However, it did not solve the more important product problem of evidence sufficiency.

The experiment reinforced the project’s broader conclusion:

```text
Retrieval quality alone does not guarantee safe AI behavior.
```

A high-consequence AI workflow must also determine:

- whether the retrieved evidence answers the exact question
- whether the evidence is complete enough
- whether source conflict is preserved
- whether uncertainty is represented accurately
- whether the model is authorized to make the requested decision

For the tested workflow, sparse retrieval remained the default generation path, while hybrid retrieval was documented as a useful evaluated alternative.

## Product Explanation

This experiment showed that hybrid retrieval improved evidence coverage but did not automatically improve answer safety. Reciprocal Rank Fusion helped surface both sides of a source conflict, yet it also preserved compliance-adjacent evidence for unsupported allegations. The product decision was therefore to keep sparse retrieval as the default for the tested workflow and treat hybrid retrieval as a targeted option for multi-source or conflict-oriented questions rather than a universal upgrade.
