import os
import sys
import requests
from datetime import datetime


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["AUTH0_REFRESH_TOKEN"]


TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"


def log(message):
    print(f"[{datetime.now().isoformat(timespec='seconds')}] {message}")


def refresh(refresh_token):
    response = requests.post(
        TOKEN_URL,
        headers={
            "content-type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token,
        },
        timeout=30,
    )

    return response


def main():

    print("=" * 78)
    print("PROJECT 4 — SCREENSHOT 6")
    print("AUTH0 REFRESH TOKEN ROTATION / REPLAY PROTECTION")
    print("=" * 78)

    log("Testing currently valid refresh token")

    # ---------------------------------------------------------
    # TEST 1 — use the valid refresh token
    # ---------------------------------------------------------

    first = refresh(REFRESH_TOKEN)

    print()
    print("-" * 78)
    print("TEST 1 — FIRST REFRESH TOKEN EXCHANGE")
    print("-" * 78)

    print(f"HTTP STATUS: {first.status_code}")

    if first.status_code != 200:
        print("RESULT: FAIL")
        print("The refresh token was not accepted.")
        print(first.text)
        sys.exit(1)

    body = first.json()

    new_refresh_token = body.get("refresh_token")

    if not new_refresh_token:
        print("RESULT: FAIL")
        print("Auth0 did not return a new refresh token.")
        sys.exit(1)

    print("OLD REFRESH TOKEN: ACCEPTED")
    print("NEW REFRESH TOKEN: ISSUED")
    print("ROTATION: SUCCESS")


    # ---------------------------------------------------------
    # TEST 2 — replay the OLD refresh token
    # ---------------------------------------------------------

    print()
    print("-" * 78)
    print("TEST 2 — REPLAY OLD REFRESH TOKEN")
    print("-" * 78)

    replay = refresh(REFRESH_TOKEN)

    print(f"HTTP STATUS: {replay.status_code}")

    try:
        replay_body = replay.json()
    except Exception:
        replay_body = {}

    error = replay_body.get("error", "")

    print(f"ERROR: {error or 'none'}")

    if replay.status_code >= 400:
        print()
        print("OLD REFRESH TOKEN: REJECTED")
        print("REPLAY PROTECTION: ACTIVE")
        print()
        print("=" * 78)
        print("RESULT: PASS")
        print("Rotated refresh-token replay was rejected.")
        print("=" * 78)

    else:
        print()
        print("OLD REFRESH TOKEN: ACCEPTED")
        print()
        print("=" * 78)
        print("RESULT: FAIL")
        print("Refresh-token replay was not rejected.")
        print("=" * 78)

        sys.exit(1)


if __name__ == "__main__":
    main()