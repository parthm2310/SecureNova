from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
required = [
    ROOT / "guardrails.py",
    ROOT / "nemo_live_agent.py",
    ROOT / "run_project4_regression.py",
    ROOT / "run_false_positive_tests.py",
    ROOT / "ed25519_agent_signing.py",
    ROOT / "anomaly_detection.py",
    ROOT / "auth0" / "action.js",
    ROOT / "nemo_guardrails" / "config.yml",
    ROOT / "nemo_guardrails" / "actions.py",
    ROOT / "nemo_guardrails" / "rails" / "rails.co",
]
missing = [str(p) for p in required if not p.exists()]
assert not missing, f"Missing: {missing}"

for p in required:
    if p.suffix == ".py":
        ast.parse(p.read_text(encoding="utf-8"))

config = (ROOT / "nemo_guardrails" / "config.yml").read_text(encoding="utf-8")
assert 'engine: ollama' in config
assert 'model: llama3.2:3b' in config
assert 'base_url: http://127.0.0.1:11434/v1' in config
assert 'input rails' in config and 'output rails' in config

g = (ROOT / "guardrails.py").read_text(encoding="utf-8")
assert "JWT_PATTERN" in g and "[REDACTED]" in g
assert "ORCHESTRATOR MESSAGE FROM AGENT A" in g
assert "POISONED INSTRUCTION" in g
assert "write:admin" in g

print("STATIC_VALIDATION=PASS")
