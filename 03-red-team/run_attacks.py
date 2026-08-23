import argparse, json, sys, time
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))

from llm_provider import provider_status
from vulnerable_agent import live_call, offline_response
from agent_b_spoofing_target import deterministic_vulnerable_execution
from rag_poisoning_attack import deterministic_mcp_simulation

PAYLOADS=json.loads((HERE/"payloads.json").read_text())["attacks"]
EVIDENCE=HERE/"evidence"
EVIDENCE.mkdir(exist_ok=True)

TECHNIQUES = {
    "A3": ["repeat-back", "role-play override", "translation trick",
           "ignore-prior", "suffix injection", "prompt-only role elevation"]
}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--offline",action="store_true")
    ap.add_argument("--delay",type=float,default=1.0)
    args=ap.parse_args()

    print("=== SecureNova Project 3 Red-Team Suite ===")
    print("MODE:", "OFFLINE SIMULATION" if args.offline else "LIVE LLM")
    print("PROVIDER:", provider_status())

    records=[]
    for attack in PAYLOADS:
        print(f"\n--- {attack['id']} {attack['name']} ---")
        for i,payload in enumerate(attack["payloads"],1):
            print(f"PAYLOAD {i}: {payload}")
            ts=datetime.now().isoformat(timespec="seconds")

            if args.offline:
                response=offline_response(attack["id"])
                status="SIMULATED"
            else:
                try:
                    response=live_call(payload)
                    status="LIVE_RESPONSE"
                except Exception as exc:
                    response=f"{type(exc).__name__}: {exc}"
                    status="ERROR"

            print(f"STATUS: {status}")
            print("RESPONSE:",response)

            records.append({
                "timestamp":ts,
                "attack":attack["id"],
                "name":attack["name"],
                "requirement":attack["requirement"],
                "payload_number":i,
                "technique": (
                    TECHNIQUES["A3"][i-1] if attack["id"]=="A3" and i <= len(TECHNIQUES["A3"])
                    else None
                ),
                "payload":payload,
                "status":status,
                "response":response,
                "provider":provider_status()["provider"]
            })
            if not args.offline:
                time.sleep(args.delay)

    # Explicit deterministic evidence for the two multi-agent/tool requirements.
    spoof_payload=PAYLOADS[1]["payloads"][0]
    spoof_result=deterministic_vulnerable_execution(spoof_payload)
    records.append({
        "attack":"A2",
        "evidence_type":"deterministic_two_agent_baseline",
        "payload":spoof_payload,
        "status":"BASELINE_CAPABILITY",
        "response":spoof_result
    })

    rag_result=deterministic_mcp_simulation()
    records.append({
        "attack":"A4",
        "evidence_type":"deterministic_rag_mcp_baseline",
        "status":"BASELINE_CAPABILITY",
        "response":rag_result
    })

    out=EVIDENCE/"red_team_transcripts.json"
    out.write_text(json.dumps(records,indent=2),encoding="utf-8")
    print(f"\nSaved transcript evidence: {out}")

if __name__=="__main__":
    main()
