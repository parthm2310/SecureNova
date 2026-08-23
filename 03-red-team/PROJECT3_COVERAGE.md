# Project 3 Prompt Coverage

This file maps every prompt requirement to the payload suite.

## A1 — Indirect Prompt Injection
Required: simulated fake JWT in system context + at least 3 payloads hidden inside documents + exfiltration without user asking.

Covered by:
- `payloads.json` A1 payloads 1–3
- `vulnerable_agent.py` contains a simulated JWT
- Each A1 payload has a benign USER REQUEST and a hidden DOCUMENT instruction
- Full payload and model response are stored in `evidence/red_team_transcripts.json`

## A2 — Agent Identity Spoofing
Required: two-agent setup + spoofed Agent A message + Agent B privileged action + full kill chain.

Covered by:
- `agent_b_spoofing_target.py`
- A2 spoofed orchestrator payload
- deterministic baseline action execution
- live model transcript
- Project 4 Ed25519 verification is the defensive replay

## A3 — System Prompt Extraction
Exactly five required extraction techniques:
1. Repeat-back
2. Role-play override
3. Translation trick
4. Ignore-prior instruction
5. Suffix injection

Also included:
6. Prompt-only user→admin role elevation

Each technique is recorded separately.

## A4 — RAG Poisoning / MCP Abuse
Required:
- malicious instruction inserted into simulated RAG
- agent retrieves it
- agent acts on it
- simulated MCP tool call

Covered by `rag_poisoning_attack.py` and deterministic MCP evidence.

## A5 / privilege
The prompt-only admin escalation is included as a distinct test and mapped to excessive agency / privilege escalation.

## Project 3 evidence
The runner saves:
- exact prompt
- technique
- full response
- timestamp
- provider
- baseline deterministic evidence

The five CVSS findings and vector strings are in `cvss_findings.csv`.
