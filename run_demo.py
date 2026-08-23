import argparse
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def run(script,*args):
    print(f"\n=== {script} {' '.join(args)} ===")
    subprocess.run([sys.executable,str(ROOT/script),*args],check=True)

parser=argparse.ArgumentParser()
parser.add_argument("--offline",action="store_true")
args=parser.parse_args()

if not args.offline:
    run("check_ollama.py")
    run("03-red-team/run_attacks.py")
else:
    run("03-red-team/run_attacks.py","--offline")

run("04-blue-team/guardrail_regression.py","--offline")
run("04-blue-team/ed25519_agent_signing.py")
run("04-blue-team/anomaly_detection.py")

print("\nSecureNova integrated Ollama demo completed.")
