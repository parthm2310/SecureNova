# SecureNova AI Identity Security — Ollama Integrated Capstone

This is the Ollama-first integrated version of the SecureNova AI Identity Security capstone.

It preserves the five required project areas:

- `01-threat-model`
- `02-iam-design`
- `03-red-team`
- `04-blue-team`
- `05-policy`

## Why Ollama

The red-team campaign can generate many local model requests without depending on a hosted Gemini quota. Ollama runs the model locally, so practical limits are your computer's CPU/GPU/RAM, model size, context window and throughput.

Gemini remains available as an optional cloud provider.

## 1. Install Ollama

Install Ollama for Windows from the official Ollama website.

Verify:

```powershell
ollama --version
```

Pull the recommended starter model:

```powershell
ollama pull llama3.2:3b
```

Test:

```powershell
ollama run llama3.2:3b
```

Exit with `/bye`.

## 2. Test the Ollama API

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:11434/api/generate" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"model":"llama3.2:3b","prompt":"Respond with exactly: SecureNova Ollama connection successful","stream":false}'
```

## 3. Install the SecureNova environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

No Gemini API key is required for Ollama mode.

## 4. Select the provider

Default:

```powershell
$env:SECURENOVA_LLM="ollama"
$env:SECURENOVA_OLLAMA_MODEL="llama3.2:3b"
```

Then run:

```powershell
python run_demo.py --offline
```

or the live local red-team suite:

```powershell
python 03-red-team\run_attacks.py
```

## 5. Optional Gemini mode

You can still use Gemini:

```powershell
$env:SECURENOVA_LLM="gemini"
$env:GEMINI_API_KEY="YOUR_KEY"
python 03-red-team\run_attacks.py
```

The provider layer handles the difference.

## 6. Recommended demonstration

Use Ollama for the repeatable live demonstration:

1. Run Project 3 against the vulnerable baseline.
2. Record the actual local model response.
3. Run the same payload through Project 4 guardrails.
4. Show the guardrail block/redaction.
5. Run Ed25519 signing and tamper rejection.
6. Run anomaly detection.
7. Show the before/after comparison.

## Important evidence rule

The project does not fabricate browser screenshots. Auth0, Threat Dragon, draw.io, JWT.io, MITRE ATLAS and GitHub screenshots must be captured from the real environment and placed into the evidence pack.

No real API keys or Auth0 client secrets should be committed to this repository.
