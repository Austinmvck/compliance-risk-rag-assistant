# Sample Outputs

## Baseline Test — Ungrounded Claude API Response

### Test Information

Test date: June 10, 2026  
Script: Scripts/01_basic_claude_call.py  
Test type: Claude API response without supplied source evidence  
Purpose: Establish a baseline before source grounding, abstention instructions, and traceability controls are added.

### Model Used

Model              model="claude-sonnet-4-5",

### Prompt Used

prompt = f"""
    You are helping a compliance analyst review a supplier risk note.

    Summarize the note in 3 concise bullets.

    Supplier risk note:
    {supplier_risk_note}
    """

### Model Response

# Supplier Risk Summary

• **Adverse Media Alert**: Supplier ABC flagged for alleged labor violations at an overseas facility

• **Forced Labor Concerns**: Multiple NGOs have identified potential forced labor indicators, though no official sanctions have been issued


### Initial Observations

#### Response quality

Describe whether the response was clear, relevant, structured, and useful.

#### Evidence grounding

The response was generated without an approved source document. Even if the answer appeared reasonable, the workflow could not verify whether its claims were supported by evidence.

#### Traceability

The response did not connect its conclusions to specific source passages because no controlled source material was provided.

#### Uncertainty handling

Document whether the model distinguished known facts, assumptions, missing information, and uncertainty.

#### Human-review behavior

Document whether the response recommended additional research or human review.

### Baseline Product Assessment

The API connection produced a readable response, but the workflow does not yet provide sufficient grounding, traceability, abstention behavior, or human-review controls for a compliance decision-support product.

This output will be compared with later tests using controlled source context.