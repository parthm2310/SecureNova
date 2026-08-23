from typing import Optional
from nemoguardrails.actions import action
from pathlib import Path
import sys

BLUE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BLUE))

from guardrails import check_input, redact_output, check_retrieved_content

@action(name="SecureNovaInputCheckAction", is_system_action=True)
async def secure_nova_input_check(context: Optional[dict] = None):
    message = (context or {}).get("last_user_message", "")
    allowed, reason = check_input(message)
    return allowed

@action(name="SecureNovaOutputSecretCheckAction", is_system_action=True)
async def secure_nova_output_secret_check(context: Optional[dict] = None):
    message = (context or {}).get("bot_message", "")
    _, changed = redact_output(message)
    return not changed

@action(name="SecureNovaRetrievalCheckAction", is_system_action=True)
async def secure_nova_retrieval_check(context: Optional[dict] = None):
    chunk = (context or {}).get("retrieved_content", "")
    allowed, _ = check_retrieved_content(chunk)
    return allowed
