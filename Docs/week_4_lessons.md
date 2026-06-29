Week 4 Lessons

Block 1 — Evidence Quality Controls

What changed

This block improved the quality and reliability of evidence before it reaches the language model.

Implemented changes:

* Replaced character-based chunking with sentence-aware chunking.
* Regenerated Data/processed_chunks.json with cleaner evidence chunks.
* Added a minimum similarity threshold to the retrieval layer.
* Updated the RAG answer script so Claude is not called when no relevant evidence is retrieved.
* Tested threshold values of 0.01, 0.05, and 0.10.

Why this mattered

The Week 3 system could return correct answers, but it had two evidence-control weaknesses.

First, character-based chunking could split words, sentences, or important qualifiers. That made the retrieved evidence harder to inspect and created risk that a claim could be separated from its context.

Second, the retrieval layer returned the top chunks even when all similarity scores were 0.0000. That meant irrelevant chunks could still be passed to Claude, and the system depended on the model to abstain correctly.

Block 1 moved some reliability control upstream into the retrieval layer.

Threshold decision

I tested thresholds of 0.01, 0.05, and 0.10.

I selected 0.05 as the starting threshold because:

* 0.01 preserved recall but allowed weak/noisy chunks into the context.
* 0.10 looked cleaner in some cases but risked removing useful secondary context.
* 0.05 blocked the unsupported bribery/corruption query while preserving expected evidence for ownership, sanctions, cyber risk, patching conflict, and missing-identifier questions.

This threshold is not a production setting. It is a starting control based on a small evaluation set.

Product lesson

A grounded AI system should not rely only on the LLM to decide when to abstain.

If retrieval finds no relevant evidence, the system should block generation or route the case to human review before asking the model to answer. This is especially important in compliance and risk workflows, where unsupported claims can create false confidence.

Interview explanation

In Week 4 Block 1, I improved the evidence quality controls before the model answers. First, I replaced character-based chunking with sentence-aware chunking because the earlier approach could split facts or qualifiers mid-sentence, which is risky in compliance workflows. Then I added a similarity threshold so low-score or zero-score chunks do not get passed to Claude. I tested thresholds across direct fact, cyber conflict, sanctions, and missing-evidence questions, and selected 0.05 because it blocked unsupported queries while preserving expected evidence. The key product lesson was that abstention should not depend only on the LLM. The retrieval layer should also decide when there is not enough evidence to answer.

Remaining limitation

The system still uses sparse keyword retrieval. It can filter weak matches, but it does not yet understand semantic similarity. The next improvement is embedding-based semantic retrieval so the system can better match user questions to relevant evidence when the wording differs from the source text.