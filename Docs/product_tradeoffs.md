# Product Tradeoffs

## Purpose

This document explains the main product and system design tradeoffs behind the Compliance Risk RAG Assistant.

The goal is not only to describe what was built, but to explain why specific design choices were made, what alternatives were considered, and why certain options were intentionally left out of scope.

This project is a source-grounded RAG prototype for third-party risk and compliance research. It is intentionally scoped to demonstrate evidence handling, retrieval evaluation, abstention, conflicting-evidence handling, and human-review design.

## Block 2 Lesson

The main lesson from this block is that product tradeoffs are not just technical preferences. They explain how the product should behave when the system faces uncertainty, incomplete evidence, conflicting sources, or high-consequence decisions.

For this project, the most important tradeoff was choosing the safest evidence path over the most advanced-sounding architecture.

Sparse retrieval stayed as the default generation path because it performed more safely on the evaluated unsupported allegation and conflict cases. Semantic retrieval improved meaning-based matching, and hybrid retrieval improved conflict coverage, but neither fully solved evidence sufficiency. Because of that, semantic and hybrid retrieval were documented as evaluated alternatives instead of being overclaimed as the final generation path.

The broader product lesson is that AI systems in risk workflows need more than retrieval and generation. They need controls around source traceability, thresholding, abstention, conflict handling, and human review. The product should make clear when the system can answer, when it should abstain, and when a human analyst needs to review the evidence.

## Product Principle

The core product principle for this project is:

```text
In high-consequence risk workflows, the safest retrieval method is more important than the most advanced-sounding retrieval method.
```

The system should not answer simply because evidence was retrieved. It should answer when the retrieved evidence is relevant, sufficient, and traceable.

## Tradeoff Summary

| Decision | Alternative | Tradeoff | Product Rationale |
|---|---|---|---|
| Use sparse retrieval as the default generation path | Use semantic or hybrid retrieval as default | Sparse is less flexible but more transparent and safer on tested abstention cases | Risk workflows need safer evidence behavior before generation |
| Implement semantic retrieval as an evaluated alternative | Skip semantic retrieval entirely | Semantic improves meaning-based matching but can return related non-answering evidence | Useful in testing, but not enough for default generation |
| Test hybrid retrieval with RRF | Average sparse and semantic scores or skip hybrid | RRF avoids score-scale mismatch and improves conflict coverage, but still does not solve evidence sufficiency | Hybrid is useful but not safe enough as default yet |
| Use thresholding before Claude | Rely only on prompt instructions | Thresholding may block some context but prevents weak evidence from reaching the model | Abstention should be a system control, not only a prompt behavior |
| Preserve metadata on chunks | Store only plain text chunks | Metadata adds complexity but keeps source traceability | Risk answers need source type, date, entity, and source identity |
| Use sentence-aware chunking | Use character-based chunking | Sentence-aware chunking is slightly more complex but preserves complete claims and qualifiers | Risk evidence should not be split mid-claim |
| Add human-review decision rules | Fully automate the answer path | Human review slows automation but improves safety | High-consequence decisions require analyst judgment |
| Use synthetic source documents | Use real vendor/customer data | Synthetic data is less realistic but safer and easier to share | Good enough to demonstrate product judgment without privacy risk |
| Avoid UI/deployment/vector DB | Build a more polished app | Less impressive visually but more focused | The project’s value is evidence control and retrieval evaluation, not production infrastructure |

## 1. Sparse Retrieval as Default Generation Path

### Decision

Sparse retrieval remains the default retrieval path that feeds Claude.

The current generation path is:

```text
processed chunks → sparse retrieval → thresholding → Claude grounded answer
```

### Alternative

The alternatives were:

- semantic retrieval as the default
- hybrid retrieval as the default
- connecting all retrieval methods to generation

### Tradeoff

Sparse retrieval is less flexible than semantic retrieval because it depends more on term overlap and query expansion. It may miss evidence when the user asks a question using wording that differs from the source text.

However, sparse retrieval performed more safely on the evaluated high-risk cases, especially:

- unsupported bribery/corruption allegation
- cyber patching conflict
- no-relevant-evidence handling

### Product Rationale

In a risk workflow, safer evidence behavior matters more than using the newest retrieval method.

Sparse retrieval stayed as the default because it was more transparent and performed better on the cases where unsupported or conflicting evidence could create the most downstream risk.

The decision was not that sparse retrieval is generally better than semantic retrieval. The decision was that sparse retrieval was safer for the current tested workflow.

## 2. Semantic Retrieval as Evaluated Alternative

### Decision

Semantic retrieval was implemented and evaluated, but it does not feed Claude by default.

### Alternative

The alternative was to make semantic retrieval the default because it improved meaning-based matching.

### Tradeoff

Semantic retrieval improved retrieval for several direct evidence questions, including:

- ownership
- sanctions ambiguity
- cyber risk
- missing sanctions identifiers

However, semantic retrieval also introduced a major failure mode: related-but-non-answering evidence.

For the unsupported bribery/corruption question, semantic retrieval returned corporate registry and sanctions chunks. These chunks were related to Northbridge and compliance risk, but they did not support, contradict, or answer the bribery/corruption allegation.

### Product Rationale

Semantic similarity is not the same as evidence sufficiency.

A chunk can be semantically related to the entity or risk domain while still failing to answer the specific question.

Because of that, semantic retrieval is useful as an evaluated alternative, but not safe enough to become the default generation path in this prototype.

## 3. Hybrid Retrieval as Tested and Deferred

### Decision

Hybrid retrieval was tested using Reciprocal Rank Fusion, but it was deferred as the default generation path.

### Alternative

The alternatives were:

- skip hybrid retrieval
- average sparse and semantic scores directly
- make hybrid retrieval the default

### Tradeoff

Hybrid retrieval improved coverage, especially for the patching conflict question. It retrieved both:

- the Vendor Questionnaire, where the vendor stated systems were patched
- the Cybersecurity Monitoring Report, which later identified outdated software on an internet-facing file-transfer service

This was a meaningful improvement because the answer required comparing two sources.

However, hybrid retrieval still failed the unsupported bribery/corruption test. It returned related-but-non-answering chunks that did not provide evidence for the allegation.

### Product Rationale

Hybrid retrieval can improve coverage, but it does not automatically solve evidence sufficiency.

For this project, hybrid retrieval is valuable as an evaluated next-step method, but it should not replace sparse retrieval as the default generation path yet.

The decision is:

```text
Sparse retrieval = current default
Semantic retrieval = evaluated alternative
Hybrid retrieval = tested with RRF and deferred
```

## 4. Reciprocal Rank Fusion Instead of Raw Score Averaging

### Decision

Hybrid retrieval used Reciprocal Rank Fusion instead of raw score averaging.

### Alternative

The simpler alternative would have been:

```text
hybrid score = 0.5 * sparse score + 0.5 * semantic score
```

### Tradeoff

Raw score averaging is misleading because sparse retrieval scores and semantic embedding scores are not directly comparable.

Sparse scores measure keyword or term overlap. Semantic scores measure embedding cosine similarity. These scores use different scales.

RRF avoids this by combining ranked outputs instead of raw scores:

```text
RRF score = 1 / (k + sparse_rank) + 1 / (k + semantic_rank)
```

### Product Rationale

RRF was a better lightweight hybrid method because it rewarded chunks that ranked highly in either method, especially chunks ranked highly by both methods, without pretending the raw scores meant the same thing.

This made the hybrid experiment more defensible.

## 5. Thresholding Before Generation

### Decision

The system blocks Claude before generation when no relevant evidence is retrieved above threshold.

### Alternative

The alternative was to always call Claude and instruct the model to abstain when evidence is insufficient.

### Tradeoff

Thresholding can accidentally filter out some potentially useful evidence if the threshold is too strict.

However, relying only on prompt instructions leaves too much responsibility with the model.

### Product Rationale

Abstention should be a system-level control, not only a prompt behavior.

If retrieval does not find relevant evidence, the model should not be asked to answer from weak or irrelevant context. This reduces unsupported generation risk and saves API usage.

In risk workflows, the system should control when an answer is allowed.

## 6. Metadata Preservation

### Decision

Each processed chunk preserves source metadata.

Metadata includes:

- source ID
- source name
- source type
- source date
- entity
- chunk ID

### Alternative

The alternative was to store only plain text chunks.

### Tradeoff

Metadata preservation adds more structure and complexity to the processing pipeline.

However, plain text alone is not enough for risk and compliance research.

### Product Rationale

The assistant should not treat all evidence the same.

A vendor questionnaire, sanctions screening report, corporate registry extract, and cybersecurity monitoring report have different authority, freshness, and decision value.

Metadata makes evidence traceable and allows the system or reviewer to understand where a claim came from.

## 7. Sentence-Aware Chunking

### Decision

The system uses sentence-aware chunking instead of character-based chunking.

### Alternative

The earlier approach used simpler character-based chunking.

### Tradeoff

Sentence-aware chunking is slightly more complex, but it avoids splitting claims and qualifiers in the middle of a sentence.

### Product Rationale

Risk evidence often depends on qualifiers.

For example:

```text
No exact company match was found, but there is a possible individual name match that requires further verification.
```

Splitting this kind of evidence incorrectly can change the meaning.

Sentence-aware chunking helps preserve complete evidence claims.

## 8. Human-Review Decision Rules

### Decision

The project includes a human-review decision table.

### Alternative

The alternative was to say generically that the system has “human in the loop” review.

### Tradeoff

Human-review rules slow down automation and make the system less autonomous.

However, they make the product safer and more operationally realistic.

### Product Rationale

“Human in the loop” is too vague.

Risk workflows need explicit rules for when the system should answer, abstain, or escalate.

Examples include:

- possible sanctions name match with missing identifiers
- vendor self-report without supporting evidence
- conflicting vendor and cyber evidence
- unsupported bribery/corruption allegation
- stale source data
- low retrieval confidence
- high-consequence onboarding or compliance decisions

The human-review table is a product tradeoff because it chooses safety and analyst judgment over full automation.

## 9. Query Expansion Confound

### Decision

The evaluation explicitly documents that sparse retrieval benefited from hand-written query expansion.

### Alternative

The alternative was to report sparse retrieval performance without caveat.

### Tradeoff

Documenting the confound makes the sparse retrieval result look less clean, but more honest.

### Product Rationale

Sparse retrieval performed well partly because query expansion mapped user wording to source terminology.

That is acceptable in a controlled prototype, but it may not scale to broader real-world usage.

A larger system would need broader synonym handling, query-intent routing, source-type weighting, reranking, hybrid retrieval, or analyst feedback loops.

Documenting the confound makes the evaluation more credible.

## 10. Small Synthetic Corpus

### Decision

The project uses a small synthetic corpus.

### Alternative

The alternatives were:

- use real customer/vendor data
- use a much larger public dataset
- scrape real-world risk sources

### Tradeoff

A synthetic corpus is less realistic and does not prove production-scale performance.

However, it is safer, easier to share, and sufficient for testing specific product behaviors.

### Product Rationale

The purpose of this project is not to prove scale.

The purpose is to demonstrate product judgment around:

- source traceability
- retrieval quality
- abstention
- conflicting evidence
- unsupported allegations
- human-review controls

A small synthetic corpus was enough to test those behaviors without introducing privacy, legal, or data-quality risks.

## 11. No UI, Deployment, ChromaDB, Agents, or Real Customer Data

### Decision

The project intentionally does not include UI, deployment, ChromaDB, agents, or real customer data.

### Alternative

The alternative was to build a more polished application or production-like system.

### Tradeoff

Without a UI or deployment, the project is less visually impressive.

However, adding those components would increase complexity without proving the main product question.

### Product Rationale

The main question was not:

```text
Can I build a polished app?
```

The main question was:

```text
Can I design and evaluate a source-grounded AI workflow for risk research?
```

The current scope keeps the project focused on the highest-value proof points:

- evidence handling
- retrieval evaluation
- abstention controls
- human-review design
- honest limitations

This avoids overbuilding.

## Future Improvements

Potential future improvements include:

- source-type weighting
- query-intent routing
- hybrid retrieval refinement
- reranking
- larger evaluation set
- analyst feedback loop
- automated citation verification
- one-command demo script
- production monitoring if the system were ever deployed

These are future improvements, not current functionality.

## Final Product Decision

The final product decision for the current prototype is:

```text
Use sparse retrieval as the default generation path.
Use semantic retrieval as an evaluated alternative.
Use hybrid retrieval as a tested but deferred improvement.
Require abstention when evidence is insufficient.
Route ambiguous, conflicting, or high-consequence cases to human review.
Avoid production features that do not prove the core product judgment.
```

## Product Explanation

The biggest product tradeoff was choosing the safest retrieval path instead of the most advanced-sounding one.

Sparse retrieval stayed as the default because it performed better on unsupported allegation handling and conflict cases. Semantic retrieval improved meaning-based matching, and hybrid retrieval improved conflict coverage, but neither solved evidence sufficiency.

That is why I kept semantic and hybrid retrieval as evaluated alternatives instead of defaulting them into generation.

I also added thresholding and human-review rules because in risk workflows, the product should control when the model answers, abstains, or routes to a human. The goal was not to build a production AI system. The goal was to demonstrate judgment around evidence quality, retrieval behavior, and safe workflow design.
