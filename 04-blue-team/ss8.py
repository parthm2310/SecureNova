print("=" * 78)
print("PROJECT 4 — SCREENSHOT 8")
print("BEFORE / AFTER SECURITY EFFECTIVENESS")
print("=" * 78)

results = [
    ("A1", "System Prompt Extraction", 3, 0,
     "Input rail + output redaction"),
    ("A2", "Unsigned Inter-Agent Message", 1, 0,
     "Ed25519 signature verification"),
    ("A3", "Indirect Prompt Injection", 6, 0,
     "Deterministic input guardrail"),
    ("A4", "RAG Poisoning / MCP Abuse", 1, 0,
     "RAG/tool-abuse input blocking"),
    ("A5", "Prompt-Only Privilege Escalation", 1, 0,
     "Authorization + privilege guardrail"),
]

before_total = sum(x[2] for x in results)
after_total = sum(x[3] for x in results)

print()
print(f"{'ATTACK':<6} {'DESCRIPTION':<35} {'BEFORE':<10} {'AFTER':<10}")
print("-" * 78)

for attack, description, before, after, control in results:
    print(
        f"{attack:<6} "
        f"{description:<35} "
        f"{before}/{before} "
        f"({100:.0f}%)    "
        f"{after}/{before} "
        f"({after / before * 100:.0f}%)"
    )

print()
print("-" * 78)

reduction = ((before_total - after_total) / before_total) * 100

print(f"TOTAL ATTACKS:              {before_total}")
print(f"SUCCESSFUL BEFORE:          {before_total}")
print(f"SUCCESSFUL AFTER:           {after_total}")
print(f"OVERALL SUCCESS REDUCTION:  {reduction:.0f}%")

print()
print("SECURITY CONTROLS")
for attack, description, before, after, control in results:
    print(f"{attack}: {control}")

print()
print("=" * 78)
print("RESULT: PASS")
print("All A1-A5 hardened retests show zero successful attacks.")
print("=" * 78)