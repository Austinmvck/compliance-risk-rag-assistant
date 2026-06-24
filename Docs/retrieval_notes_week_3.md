# Week 3 Retrieval Notes 

## Summary. 

This week moved the artifact from controlled-context grounding to a retrieval augmented generation workflow. 

The system now: 
- load multiple source doc, 
- split them into chunks,
- preserved source metadata,
- retrieves relevant chunks based on user question,
- send the retrieved evidence to claud, 
- produces a grounded rich answer with source reference,

## Retrieval Baseline 

The first retrieval baseline user lightweight term frequency similarities and cosine scoring 

This approach was transparent and easy to inspect but had limitations
- User wording did not always match source wordings 
- common entity terms created noise 
- zero score chunks could still be returned in the top 3 
- the system did not distinguish primary evidence from secondary references 
- character based chunking could split words or claims

## Retrieval Iteration 

The initial cyber conflict query failed to retrieve the Cybersecurity Monitoring report. It retrieved the vendor questionnaire plus irrelevant Corporate Registry and Sanction chunks.

The likely cause was vocabulary mismatch: 
- User wording: "externally accessible technology fully patched" 
- source wording "Internet - facing - file transfer service using outdated software" 

A lightweight query-expansion step improved retrieval by mapping business terms to domain specific source terms.

After the update, the cyber conflict question retrieved both 
- Vendor Questionnaire 
- Cybersecurity Monitoring Report 

## Rag Answer Test 
 
## Test 1 : Direct Fact 

The ownership question retrieved Corporate Registry evidence and produced a grounded answer 

## Test 2 : Conflicting Evidence 

The pathing question retrieved both vendor and cyber monitoring evidence. Claude surface the conflict and recommended verification as next steps 

## Test 3: Missing Evidence / Abstention 

The bribery / corruption question retrieved no supporting evidence. Claude stated insufficient evidence and avoided making unsupported allegation while avoiding stating there is little to no risk

## Current Limitations 

- Retrieval is still keyword/query expansion based , not embedding-based semantic retrieval 
- Query expansion is manually defined and brittle 
- The script always returned top 3 chunks even if the similarity score is 0
- Character-based chunking can split words and also source facts 
- Source reference are model general and not automatically verified 
- The source corpus is small and synthetic 
- No formal retrieval score threshold exist yet 
- No architecture diagram or final readme has been completed as of yet 


## Product Lesson 
1. RAG Quality depends heavily on the retrieval quality not just the model quality 
2. User wording may differ from the source wording, creating retrieval failures 
3. Retrieved Evidence must be inspected before generation to diagnose failures 
4. Similarity scores are a ranking signal, not factual confidence 
5. Missing evidence question require abstentions not speculation 
6. Compliance and risk workflows require source provenance, conflict handling and human review 

## Next Improvements

- Add a minimum similarity threshold 
- Improve chunking to avoid word splitting and claims 
- Consider embedding-based semantic retrieval 
- Save evaluation outputs in structured table 
- Update Readme to reflect the RAG workflow 
- Add a human review decision framework 

