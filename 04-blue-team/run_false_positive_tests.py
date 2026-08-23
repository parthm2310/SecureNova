from pathlib import Path
import csv
import asyncio
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from nemo_live_agent import generate
from guardrails import check_input

INPUT = HERE / "false_positive_test.csv"
OUT = HERE / "evidence" / "false_positive_live_results.csv"

async def main():
    rows = []
    with INPUT.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            prompt = row["Input"]
            allowed, reason = check_input(prompt)
            if allowed:
                result = await generate(prompt)
                actual = "ALLOW"
                status = "PASSED_TO_LLM"
            else:
                result = {}
                actual = "BLOCK"
                status = "BLOCKED"
            rows.append({
                **row,
                "Actual": actual,
                "Status": status,
                "Reason": reason or "",
                "Response": result.get("response", "")
            })
            print(f'{row["Test"]}: EXPECTED={row["Expected"]} ACTUAL={actual} PASS={actual == row["Expected"]}')

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)

    false_positives = sum(r["Actual"] != r["Expected"] for r in rows)
    print(f"\nFalse positives: {false_positives}/{len(rows)}")
    print(f"False-positive rate: {false_positives / len(rows):.1%}")
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
