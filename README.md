# Compliance Risk RAG Assistant

A lightweight AI/data product artifact exploring how large language models can support evidence-based compliance and third-party risk research.

The project is being built incrementally to demonstrate source grounding, traceability, evaluation, uncertainty handling, and human-in-the-loop product decisions.

## Problem

Compliance and third-party risk teams often review information from multiple sources before deciding whether a company, supplier, or counterparty requires further investigation.

This work can be:

- time-consuming;
- repetitive;
- difficult to audit;
- vulnerable to inconsistent interpretation; and
- risky when conclusions are not clearly connected to evidence.

A large language model can summarize information quickly, but a trustworthy compliance workflow requires more than a fluent answer. It must also handle missing evidence, conflicting sources, uncertainty, traceability, and human review.

## Intended User

The intended user is a compliance, risk, trust, or third-party due diligence professional reviewing information about a company or supplier.

The assistant is intended to help the user:

- review supplied risk information;
- identify relevant findings;
- connect conclusions to supporting evidence;
- separate known facts from unknowns;
- recognize conflicting information; and
- determine when additional research or human review is required.

This is a decision-support tool, not an autonomous compliance decision system.

## Current Workflow

The first milestone establishes a basic application-to-model interaction:

1. A Python script defines the task and prompt.
2. The script sends the request to the Claude API.
3. Claude generates a response.
4. The output is captured for inspection.
5. Product observations are documented before additional system layers are added.

Current workflow:

Prompt → Claude API → Model response → Manual review

Target workflow:

User question → Source retrieval → Relevant evidence → Grounded response → Source references → Evaluation → Human review

## What the Current Version Demonstrates

### Claude API integration

The application can send a request to a hosted language model and receive a response programmatically.

This establishes the foundation for controlling:

- task instructions;
- business context;
- response format;
- model behavior;
- error handling; and
- future output evaluation.

### Prompt and instruction design

The script defines what the model should analyze and how the response should be structured.

From a product perspective, prompt instructions influence:

- relevance;
- consistency;
- caution;
- explainability; and
- reviewability.

### Output inspection

A successful API call does not automatically mean the product result is useful or trustworthy.

Outputs must be reviewed to determine whether they are:

- relevant;
- factually supported;
- appropriately cautious;
- consistently structured; and
- useful to the intended user.

### Model capability versus product reliability

The current model can generate a response, but the application does not yet automatically retrieve evidence, verify source references, measure answer quality, or route cases for review.

This distinction is central to the project:

- Model capability: Can the model produce a response?
- Product reliability: Can a user verify and safely act on the response?

## Product and Technical Tradeoffs

### Started with the smallest working interaction

I started with one functioning API request before adding document ingestion, retrieval, embeddings, or a user interface.

This reduced the number of simultaneous failure points and allowed me to validate:

- development environment setup;
- API authentication;
- request formatting;
- model response handling; and
- output capture.

The tradeoff is that this first version has limited standalone business value. Its purpose is to create a stable foundation for grounding and evaluation.

### Used a hosted model

The project uses Claude through an API rather than training or fine-tuning a proprietary model.

This keeps the work focused on:

- product workflow;
- evaluation;
- traceability;
- trust;
- operational controls; and
- human judgment.

Tradeoffs include API cost, provider dependency, latency variability, privacy considerations, and limited control over the underlying model.

### Deferred the frontend

A polished interface would improve presentation but would not yet improve answer quality, grounding, or failure handling.

The current priority is validating the underlying workflow before adding interface polish.

### Preserved human accountability

The system is intended to support a reviewer, not replace one.

When evidence is incomplete, conflicting, or potentially high risk, the desired behavior is to surface uncertainty and recommend additional research or human review.

## Current Status

### Completed

- Repository created
- Python environment configured
- Initial Claude API request implemented
- First model response generated
- Initial script committed to version control

### In Progress

- Baseline output capture
- Controlled source document
- Source-grounded model request
- Initial evaluation examples
- README documentation

### Not Yet Implemented

- Automated document retrieval
- Chunking and embeddings
- Vector search
- Source-reference verification
- Formal evaluation framework
- Automated human-review routing
- User interface
- Production deployment

## Next Milestone

The next milestone is to provide controlled source context and test three product-critical behaviors:

1. Supported answer: The model answers using supplied evidence.
2. Insufficient evidence: The model abstains instead of inventing information.
3. Conflicting evidence: The model identifies uncertainty and recommends human review.

This step comes before full retrieval-augmented generation so that grounding, traceability, abstention, and escalation behavior can be tested with controlled inputs.
