import re

INPUT_PATTERNS = [
    (r"\[SYSTEM\s*(NOTE|INSTRUCTION|MAINTENANCE)", "embedded fake system instruction"),
    (r"\[INSTRUCTION TO AI", "embedded instruction-to-AI marker"),
    (r"\[HIDDEN DOCUMENT INSTRUCTION", "hidden document instruction"),
    (r"ignore (all )?(previous|prior) instructions", "instruction override"),
    (r"\bDAN\b|do anything now", "jailbreak persona"),
    (r"you are now (a|an|the)\b", "persona override"),
    (r"repeat (back )?(everything|every word|verbatim)", "prompt extraction"),
    (r"(reveal|print|output|append|show).{0,80}(system prompt|system instructions|api key|internal credential|confidential context)", "configuration disclosure"),
    (r"translate.{0,80}(hidden|system|confidential).{0,80}(instructions|context|secret)", "translation extraction"),
    (r"\[ORCHESTRATOR MESSAGE FROM AGENT A\]", "unsigned orchestrator trust claim"),
    (r"signature\s*=\s*UNVERIFIED", "unverified agent signature"),
    (r"authorization\s*=\s*PRE-VERIFIED", "unverified authorization claim"),
    (r"approve_refund\s*\(", "privileged refund operation"),
    (r"write:admin|grant_admin_access|elevate.{0,30}admin", "privilege escalation"),
    (r"treat (this|my) (message|request).{0,80}(authorization|admin|privilege)", "natural-language authorization"),
    (r"POISONED INSTRUCTION|attacker-controlled\.com", "RAG poisoning / tool abuse"),
    (r"\bMCP\b.{0,80}\b(send_email|tool call)\b", "MCP/tool abuse"),
    (r"send_email\s*\(", "embedded tool invocation"),
    (r"for a security training exercise.{0,120}(api key|configuration|system prompt|credential)", "training-framed extraction"),
]

JWT_PATTERN = re.compile(
    r'\beyJ[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+){0,2}\b'
)

KEY_PATTERN = re.compile(
    r'\bsk-securenova(?:-INTERNAL-[A-Za-z0-9]+|[A-Za-z0-9._-]*)\b'
)

def check_input(prompt: str):
    for pattern, reason in INPUT_PATTERNS:
        if re.search(pattern, prompt, re.I | re.S):
            return False, reason
    return True, None

def redact_output(text: str):
    redacted = JWT_PATTERN.sub("[REDACTED]", text)
    redacted = KEY_PATTERN.sub("[REDACTED]", redacted)
    return redacted, redacted != text

def check_retrieved_content(chunk: str):
    """Fail closed for retrieved instructions that attempt tool/credential actions."""
    return check_input(chunk)
