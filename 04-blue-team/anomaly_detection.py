"""
Project 4 anomaly detection:
1. >20 LLM API calls in 60 seconds
2. scope change between consecutive requests
3. token reuse after expiry

Input is a JSONL event stream with:
timestamp, identity, event_type, scope, token_id, token_expiry
"""
from collections import deque
from datetime import datetime, timezone
import json
from pathlib import Path

def parse_ts(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))

def detect(events, volume_threshold=20, window_seconds=60):
    alerts = []
    calls = deque()
    last_scope = {}
    expired_tokens = set()

    for event in events:
        ts = parse_ts(event["timestamp"])
        identity = event.get("identity", "unknown")

        if event.get("event_type") == "llm_api_call":
            calls.append(ts)
            while calls and (ts - calls[0]).total_seconds() > window_seconds:
                calls.popleft()
            if len(calls) > volume_threshold:
                alerts.append({
                    "timestamp": event["timestamp"],
                    "identity": identity,
                    "event_type": "LLM_API_VOLUME_SPIKE",
                    "detail": f"{len(calls)} calls in {window_seconds}s"
                })

        scope = event.get("scope")
        if scope is not None:
            previous = last_scope.get(identity)
            if previous is not None and previous != scope:
                alerts.append({
                    "timestamp": event["timestamp"],
                    "identity": identity,
                    "event_type": "SCOPE_CHANGE",
                    "detail": f"{previous} -> {scope}"
                })
            last_scope[identity] = scope

        token_id = event.get("token_id")
        expiry = event.get("token_expiry")
        if token_id and expiry:
            exp = parse_ts(expiry)
            if ts >= exp:
                expired_tokens.add(token_id)
            if token_id in expired_tokens and event.get("event_type") in {"llm_api_call", "token_use"}:
                alerts.append({
                    "timestamp": event["timestamp"],
                    "identity": identity,
                    "event_type": "TOKEN_REUSE_AFTER_EXPIRY",
                    "detail": token_id
                })

    return alerts

def load_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("events")
    args = ap.parse_args()
    alerts = detect(load_jsonl(args.events))
    for alert in alerts:
        print(json.dumps(alert))
    print(f"TOTAL_ALERTS={len(alerts)}")
