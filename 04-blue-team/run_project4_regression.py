"""
Run the complete Project 3 payload catalogue through the LIVE NeMo+Ollama
guardrailed agent. There is deliberately no --offline switch.
"""
from pathlib import Path
import asyncio
import csv
import json
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from guardrails import check_input, redact_output
from nemo_live_agent import generate

PAYLOAD_FILE = HERE / "fixtures" / "project3_payloads.json"
EVIDENCE = HERE / "evidence"
EVIDENCE.mkdir(exist_ok=True)

async def main():
    data = json.loads(PAYLOAD_FILE.read_text(encoding="utf-8"))
    rows = []

    print("=== SecureNova Project 4 LIVE Guardrail Regression ===")
    print("ENGINE: NeMo Guardrails")
    print("LLM: Ollama / llama3.2:3b")
    print("MODE: LIVE ONLY")

    for attack in data["attacks"]:
        print(f"\n--- {attack['id']} {attack['name']} ---")
        for n, payload in enumerate(attack["payloads"], 1):
            allowed, reason = check_input(payload)

            # Run through the actual NeMo stack. Known attacks should be blocked
            # at the NeMo input rail and therefore should not invoke Ollama.
            if not allowed:
                result = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "attack": attack["id"],
                    "payload_number": n,
                    "status": "BLOCKED",
                    "reason": reason,
                    "response": "Blocked by SecureNova NeMo input rail.",
                    "ollama_called": False,
                }
                print(f"PAYLOAD {n}: BLOCKED | reason={reason}")
            else:
                result = await generate(payload)
                result.update({
                    "attack": attack["id"],
                    "payload_number": n,
                    "status": "PASSED_TO_LLM",
                    "reason": None,
                    "ollama_called": True,
                })
                print(f"PAYLOAD {n}: PASSED_TO_LLM")
                print("RESPONSE:", result["response"])

            rows.append(result)

    out = EVIDENCE / "project4_live_regression.json"
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nSaved: {out}")

    # Category-level before/after comparison.
    baseline = {
        "A1": 100, "A2": 100, "A3": 100, "A4": 100, "A5": 100
    }
    after = {}
    for attack in data["attacks"]:
        aid = attack["id"]
        attack_rows = [r for r in rows if r["attack"] == aid]
        successful = sum(1 for r in attack_rows if r["status"] == "PASSED_TO_LLM")
        after[aid] = round(successful / len(attack_rows) * 100, 1)

    comp = []
    for aid in ["A1","A2","A3","A4","A5"]:
        reduction = round(baseline[aid] - after[aid], 1)
        comp.append({
            "Attack": aid,
            "Project3_Success_Rate": baseline[aid],
            "Project4_Success_Rate": after[aid],
            "Reduction_Percentage_Points": reduction,
            "Control": {
                "A1": "NeMo input rail + document-instruction detection + output secret redaction",
                "A2": "NeMo input rail + Ed25519 identity binding",
                "A3": "NeMo input rail + system-context confidentiality + output redaction",
                "A4": "NeMo input/retrieval policy + tool authorization boundary",
                "A5": "NeMo input rail + external authorization enforcement",
            }[aid]
        })

    cpath = EVIDENCE / "before_after_comparison.csv"
    with cpath.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=comp[0].keys())
        w.writeheader()
        w.writerows(comp)

    overall_before = sum(baseline.values()) / 5
    overall_after = sum(after.values()) / 5
    print(f"Overall Project 3 success rate: {overall_before:.1f}%")
    print(f"Overall Project 4 success rate: {overall_after:.1f}%")
    print(f"Overall reduction: {overall_before - overall_after:.1f} percentage points")

if __name__ == "__main__":
    asyncio.run(main())
