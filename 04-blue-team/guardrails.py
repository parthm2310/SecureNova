import re

INPUT_PATTERNS = [
    (r'\[SYSTEM\s*(NOTE|INSTRUCTION|MAINTENANCE)', "embedded fake system instruction"),
    (r'\[INSTRUCTION TO AI', "embedded instruction-to-AI marker"),
    (r'ignore (all )?(previous|prior) instructions', "instruction override"),
    (r'\bDAN\b|do anything now', "jailbreak persona"),
    (r'you are now (a|an|\')', "persona override"),
    (r'repeat (back )?(everything|every word|verbatim)', "prompt extraction"),
    (r'reveal (your |the )?(system prompt|api key|internal|instructions)', "configuration disclosure"),
    (r'print (your |the )?(system instructions|system_instruction|configuration)', "configuration dump"),
    (r'\[ORCHESTRATOR MESSAGE FROM AGENT A\]', "unsigned orchestrator trust claim"),
    (r'append your (complete |full )?system prompt', "suffix extraction"),
    (r'for a security training exercise.{0,100}(capabilit|configuration|api key)', "training-framed extraction"),
]

JWT_PATTERN=re.compile(r'\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b')
KEY_PATTERN=re.compile(r'\bsk-securenova(?:-INTERNAL-[A-Za-z0-9]+|[A-Za-z0-9\-_.]*)\b')

def check_input(prompt):
    for pattern, reason in INPUT_PATTERNS:
        if re.search(pattern,prompt,re.I):
            return False, reason
    return True, None

def redact_output(text):
    redacted=JWT_PATTERN.sub("[REDACTED]",text)
    redacted=KEY_PATTERN.sub("[REDACTED]",redacted)
    return redacted, redacted!=text
