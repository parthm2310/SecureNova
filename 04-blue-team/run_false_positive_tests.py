import csv
from pathlib import Path
from guarded_agent import guarded_send

HERE = Path(__file__).resolve().parent
input_file = HERE / "false_positive_test.csv"
output_file = HERE / "evidence_false_positive_results.csv"

results = []

with input_file.open("r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        prompt = row["Input"]
        expected = row["Expected"]

        result = guarded_send(prompt)

        actual = "ALLOW" if result["status"] == "PASSED_TO_LLM" else "BLOCK"
        passed = actual == expected

        print(f'{row["Test"]}: EXPECTED={expected} ACTUAL={actual} PASS={passed}')

        results.append({
            "Test": row["Test"],
            "Input": prompt,
            "Expected": expected,
            "Actual": actual,
            "Pass": passed,
            "Status": result["status"],
            "Reason": result["reason"] or ""
        })

with output_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["Test", "Input", "Expected", "Actual", "Pass", "Status", "Reason"]
    )
    writer.writeheader()
    writer.writerows(results)

passed = sum(r["Pass"] for r in results)

print()
print(f"Passed: {passed}/{len(results)}")
print(f"False positives: {len(results) - passed}")
print(f"Results saved to: {output_file}")