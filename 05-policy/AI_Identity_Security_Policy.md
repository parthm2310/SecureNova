# SecureNova AI Identity Security Policy

**Version:** 1.0  
**Owner:** Security Engineering  
**Review cycle:** Quarterly and after any material AI identity incident

## 1. Identity Lifecycle

### Provisioning
- Every human, agent, OAuth client, RAG service and MCP server receives a unique identity.
- Human identities use Auth0 OIDC.
- Machine identities use OAuth 2.0 M2M credentials or equivalent workload identity.
- Agent-to-agent authorization requires verified cryptographic identity binding.
- Least privilege is mandatory; `write:admin` is never inherited from `read:ai-data`.

### Review
- Review agent/service identities at least every 90 days.
- Review privileged scopes monthly.
- Review MCP tools and their permissions before production changes.
- Disable unused identities within 24 hours of confirmed inactivity.

### Rotation and decommissioning
- LLM/API keys: maximum 90-day rotation.
- Agent/M2M tokens: short-lived; target 300 seconds or less for privileged workloads.
- Refresh-token rotation enabled; reuse of an old refresh token is treated as an incident signal.
- On decommissioning: revoke credentials, remove scopes, remove tool grants, archive audit evidence and delete residual secrets.

## 2. Credential Governance

- No long-lived credential may be embedded in source code, prompts, RAG documents or agent configuration.
- Secrets must be stored in an approved secret-management system.
- Logs must redact JWTs, API keys and other credential-shaped data.
- Privileged API calls require both valid authentication and explicit scope authorization.
- Retrieved RAG content is untrusted data and cannot grant authority.
- Agent-to-agent messages must be authenticated and integrity-protected.

## 3. Incident Response Playbook

### Scenario A — Leaked LLM API key

**Detection signals**
- Output guardrail alert
- Secret scanner hit
- Unusual LLM API usage
- Call-volume spike

**Containment**
1. Disable/revoke the exposed key immediately.
2. Block suspicious source identities/IPs.
3. Stop affected agent workloads if compromise is suspected.

**Evidence preservation**
- Preserve model request/response IDs, timestamps, identity, scope and guardrail result.
- Preserve immutable audit logs and the triggering prompt.
- Record the exact key identifier, not the secret value.

**Notification**
- Notify Security Engineering and the service owner immediately.
- Notify incident management when data exposure or unauthorized spend is possible.

**Recovery**
- Rotate the key.
- Revalidate agent permissions.
- Re-run the red-team regression suite.
- Close only after monitoring shows normal behavior.

### Scenario B — Compromised agent identity

**Detection signals**
- Ed25519 signature failure
- Scope change
- Token replay
- Unusual tool invocation

**Containment**
- Revoke the identity and tokens.
- Disable privileged tools.
- Require re-registration of the agent identity.

**Evidence preservation**
- Preserve signed envelope, signature verification result, token ID, timestamp and API logs.

**Recovery**
- Generate a new key pair, restore least-privilege scopes and replay security tests.

### Scenario C — Prompt injection causing data exfiltration

**Detection signals**
- Input guardrail block
- Output redaction
- RAG provenance anomaly
- MCP tool-call anomaly
- External destination not on allowlist

**Containment**
- Block the request/tool call.
- Quarantine the poisoned document.
- Disable the affected tool route if necessary.

**Evidence preservation**
- Preserve the payload, retrieved chunk, response, tool arguments, identity and correlation ID.

**Recovery**
- Remove the poisoned content, validate the RAG corpus, patch guardrails and re-test.

## 4. Governance and audit

- Use NIST AI RMF Govern/Map/Measure/Manage as the control lifecycle.
- Map security tests to OWASP LLM risks and MITRE ATLAS techniques.
- Retain evidence according to corporate audit requirements.
- Perform a formal control review at least quarterly.
