# Week 1 Notes — Claude API Fundamentals

## Block 1: Setup + First Claude API Call

### What I Built

I created a local Python project connected to GitHub and successfully ran my first direct Claude API call.

The script `Scripts/01_basic_claude_call.py` sends a supplier-risk note to Claude and returns a short compliance-style summary.

### Files Created / Used

- `Scripts/01_basic_claude_call.py` — first direct Claude API script
- `.env` — stores the real Anthropic API key locally
- `.env.example` — safe placeholder showing required environment variable
- `.gitignore` — prevents `.env`, `.venv`, and local machine files from being committed
- `requirements.txt` — lists Python dependencies
- `Outputs/sample_outputs.md` — stores sample output from the first script

### What Happened Technically

The script loaded the API key from `.env`, created an Anthropic client, sent a prompt to Claude, and printed the returned response in Terminal.

The basic flow was:

1. Local Python script runs.
2. `.env` loads the Anthropic API key.
3. The Anthropic client authenticates the request.
4. The prompt is sent to the Claude model.
5. Claude returns a response.
6. The script prints the response in Terminal.

### Errors I Hit

#### Error 1: Invalid API Key

I got a `401 invalid x-api-key` error.

Cause: `.env` still contained a placeholder value instead of a real Anthropic API key.

Product takeaway: AI workflows depend on correct secrets and environment configuration. Bad credentials break the integration before the model can do anything useful.

#### Error 2: Model Not Found

I got a `404 model not found` error.

Cause: The model name in the script was not valid for my API/account.

Product takeaway: External AI providers can change model names, model access, and version availability. Product teams need model/version awareness, fallback behavior, and clear error handling.

### PM Takeaways

- A direct LLM API call is the foundation of most applied AI workflows.
- Freeform model output can be useful, but it is not automatically product-ready.
- Risk/compliance workflows need structured outputs, source evidence, confidence, and human-review logic.
- Authentication, model configuration, and provider dependencies are real product risks.
- The next step is to move from loose text output to structured output.