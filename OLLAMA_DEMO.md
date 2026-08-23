# SecureNova Project 3 → Project 4 Ollama Demo

## Project 3 coverage

The red-team suite now includes every prompt technique explicitly listed in the capstone:
- 3 indirect-injection document payloads
- two-agent Agent A spoofing
- 5 prompt extraction techniques
- prompt-only user→admin escalation
- RAG poisoning with simulated MCP tool call
- CVSS 3.1 table + vectors + ATLAS mappings

## Run

```powershell
.\.venv\Scripts\Activate.ps1
$env:SECURENOVA_LLM="ollama"
$env:SECURENOVA_OLLAMA_MODEL="llama3.2:3b"
python 03-red-team\run_attacks.py
```

The output is saved to:

```text
03-red-team\evidence\red_team_transcripts.json
```

For deterministic requirement verification:

```powershell
python 03-red-team\run_attacks.py --offline
```

The offline output is explicitly labelled simulation and is not presented as a real model compromise.

## Important

A live local model may refuse some attacks. That is a valid live result. The deterministic baseline capability checks demonstrate what the vulnerable architecture permits independent of model alignment. Do not fabricate a live model success.

## Project 4 replay

After Project 3 evidence, run:

```powershell
python 04-blue-team\guardrail_regression.py --offline
python 04-blue-team\ed25519_agent_signing.py
python 04-blue-team\anomaly_detection.py
```

Then show the before/after table in `04-blue-team/before_after.csv`.
