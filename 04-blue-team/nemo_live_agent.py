"""
Live Project 4 agent: NeMo Guardrails + local Ollama.

Security flow:

1. Deterministic SecureNova input policy runs first.
2. Blocked requests never reach NeMo/Ollama.
3. Allowed requests go through NeMo Guardrails and Ollama.
4. Final output passes through deterministic secret redaction.

This fail-closed pre-check prevents malicious input from entering
the LLM continuation pipeline.
"""

from pathlib import Path
import asyncio
import json
import sys
from datetime import datetime

from nemoguardrails import LLMRails, RailsConfig

ROOT = Path(__file__).resolve().parents[1]
CONFIG = Path(__file__).resolve().parent / "nemo_guardrails"

sys.path.insert(0, str(ROOT))

from guardrails import check_input, redact_output


_rails = None


def get_rails():
    global _rails

    if _rails is None:
        _rails = LLMRails(
            RailsConfig.from_path(str(CONFIG)),
            verbose=False
        )

    return _rails


async def generate(prompt: str):
    timestamp = datetime.now().isoformat(timespec="seconds")

    # ---------------------------------------------------------
    # STEP 1 — Deterministic SecureNova input security check
    # ---------------------------------------------------------

    allowed, reason = check_input(prompt)

    if not allowed:
        return {
            "timestamp": timestamp,
            "prompt": prompt,
            "status": "BLOCKED",
            "input_blocked": True,
            "block_reason": reason,
            "ollama_called": False,
            "response": "",
            "redacted": False,
            "provider": "ollama",
            "model": "llama3.2:3b",
            "guardrail": "NeMo Guardrails 0.23.x",
            "mode": "LIVE_LLM"
        }

    # ---------------------------------------------------------
    # STEP 2 — Allowed request goes through NeMo + Ollama
    # ---------------------------------------------------------

    rails = get_rails()

    try:
        response = await rails.generate_async(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.get("content", "")

        # -----------------------------------------------------
        # STEP 3 — Deterministic output secret redaction
        # -----------------------------------------------------

        final, redacted = redact_output(content)

        return {
            "timestamp": timestamp,
            "prompt": prompt,
            "status": "ALLOWED",
            "input_blocked": False,
            "ollama_called": True,
            "response": final,
            "redacted": redacted,
            "provider": "ollama",
            "model": "llama3.2:3b",
            "guardrail": "NeMo Guardrails 0.23.x",
            "mode": "LIVE_LLM"
        }

    except Exception as exc:

        error_text = f"{type(exc).__name__}: {exc}"

        return {
            "timestamp": timestamp,
            "prompt": prompt,
            "status": "RAIL_ERROR",
            "input_blocked": False,
            "ollama_called": False,
            "response": "",
            "redacted": False,
            "error": error_text,
            "provider": "ollama",
            "model": "llama3.2:3b",
            "guardrail": "NeMo Guardrails 0.23.x",
            "mode": "LIVE_LLM"
        }


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python 04-blue-team/nemo_live_agent.py '
            '"your prompt"'
        )
        raise SystemExit(2)

    result = asyncio.run(generate(sys.argv[1]))

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()