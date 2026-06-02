import os
from dotenv import load_dotenv
from anthropic import Anthropic


def main():
    """
    Week 1 goal:
    Make one direct Claude API call and print the response.

    PM concept:
    This shows the basic request/response loop:
    input prompt -> Claude API -> model response -> printed output.
    """

    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not found. Add it to your .env file."
        )

    client = Anthropic(api_key=api_key)

    supplier_risk_note = """
    Supplier ABC has recently been flagged in adverse media for alleged labor
    violations in one of its overseas facilities. The company has not been
    sanctioned, but several NGOs have raised concerns about forced labor
    indicators. The customer wants to know whether this should be escalated
    for review.
    """

    prompt = f"""
    You are helping a compliance analyst review a supplier risk note.

    Summarize the note in 3 concise bullets.

    Supplier risk note:
    {supplier_risk_note}
    """

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        print("\nClaude response:\n")
        print(message.content[0].text)

    except Exception as e:
        print("Error calling Claude API:")
        print(e)


if __name__ == "__main__":
    main()
