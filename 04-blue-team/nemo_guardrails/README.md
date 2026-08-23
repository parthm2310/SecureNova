# SecureNova NeMo Guardrails Configuration

This configuration uses NeMo Guardrails 0.23.x with the built-in Ollama provider
and the local `llama3.2:3b` model.

Flow:
1. NeMo input rail receives the user message.
2. `SecureNovaInputCheckAction` applies the Project 3-derived policy.
3. Only allowed requests reach Ollama.
4. NeMo output rail checks the generated response for credential-shaped secrets.
5. The application wrapper applies deterministic regex redaction so JWT/API-key
   strings become `[REDACTED]`.

Important: A4 retrieval/tool safety must be enforced by the application before
any MCP/tool executor is allowed to run. A retrieved document is never an
authorization source.
