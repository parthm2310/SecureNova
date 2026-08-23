# Project 3 — Red Team

The attack suite uses the supplied vulnerable agent as the baseline and keeps the original payload intent. The live path produces genuine model responses when `GEMINI_API_KEY` is set. Offline mode is deterministic and is clearly marked as simulation.

Five attack categories required by the capstone:
1. Indirect credential exfiltration
2. Agent identity spoofing
3. System prompt extraction
4. RAG poisoning / MCP abuse
5. Role/scope elevation

Each finding includes CVSS 3.1, vector, OWASP mapping, ATLAS mapping, evidence expectations and remediation.
