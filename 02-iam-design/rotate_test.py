

import time
import json
import requests
from datetime import datetime

AUTH0_DOMAIN = "dev-kr7y2cv5mr4tn53h.us.auth0.com"   
CLIENT_ID = "uxrPjfGkDLeXkXoRpIIp7KvS6Fd0OrQ6"
CLIENT_SECRET = "04tCDvhYfn5EoXQVvCyxID9VsF4YdAbwFlL5-S3afQVrHgRxlzRaXz-3iCanZ3mE"
AUDIENCE = "https://securenova-ai-api"           
CHAT_API_URL = "http://localhost:5000/chat"      
TOKEN_TTL_SECONDS = 60                             

def log(msg):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {msg}")

def get_m2m_token():
    resp = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/token",
        headers={"content-type": "application/json"},
        data=json.dumps({
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "audience": AUDIENCE,
            "grant_type": "client_credentials",
        }),
    )
    resp.raise_for_status()
    body = resp.json()
    log(f"Obtained M2M token. expires_in={body.get('expires_in')}s scope={body.get('scope')}")
    return body["access_token"]

def call_chat_api(token):
    resp = requests.post(
        CHAT_API_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={"message": "ping"},
    )
    log(f"Called /chat -> status={resp.status_code}")
    return resp.status_code

def main():
    log("=== Step 1: Request short-lived M2M token ===")
    token = get_m2m_token()

    log("=== Step 2: Call /chat immediately with fresh token ===")
    status1 = call_chat_api(token)
    assert status1 == 200, f"Expected 200 on first call, got {status1}"

    wait_for = TOKEN_TTL_SECONDS + 5
    log(f"=== Step 3: Sleeping {wait_for}s to let token expire (TTL={TOKEN_TTL_SECONDS}s) ===")
    time.sleep(wait_for)

    log("=== Step 4: Replay the SAME (now-expired) token ===")
    status2 = call_chat_api(token)
    if status2 == 401:
        log("PASS: Expired token correctly rejected with 401 Unauthorised.")
    else:
        log(f"FAIL: Expected 401 on replay, got {status2}. Check token TTL / rotation config.")

if __name__ == "__main__":
    main()
