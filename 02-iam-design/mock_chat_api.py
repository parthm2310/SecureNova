"""
SecureNova - Project 2 Step 4: Minimal Protected API for Credential Rotation Demo
A tiny local Flask server that actually validates Auth0-issued JWTs against
your tenant's real JWKS (signature, issuer, audience, expiry). This gives
rotate_test.py a genuine endpoint to call instead of a placeholder URL.

Usage:
    pip install flask pyjwt cryptography requests
    python mock_chat_api.py
    (leave this running in one terminal, run rotate_test.py in a second terminal)
"""

from flask import Flask, request, jsonify
import jwt
from jwt import PyJWKClient

app = Flask(__name__)

# ---- Fill in your real values (same as rotate_test.py) ----
AUTH0_DOMAIN = "dev-kr7y2cv5mr4tn53h.us.auth0.com"          # e.g. dev-kr7y2cv5mr4tn53h.us.auth0.com
AUDIENCE = "https://securenova-ai-api"

jwks_client = PyJWKClient(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")

@app.route("/chat", methods=["POST"])
def chat():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "missing_token"}), 401

    token = auth_header.split(" ", 1)[1]
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token_expired"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"error": "invalid_token", "detail": str(e)}), 401

    return jsonify({
        "message": "pong",
        "authenticated_client": payload.get("azp"),
        "scope": payload.get("scope"),
    }), 200
@app.route("/admin/action", methods=["POST"])
def admin_action():
    auth_header = request.headers.get("Authorization", "")

    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "missing_token"}), 401

    token = auth_header.split(" ", 1)[1]

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "token_expired"}), 401

    except jwt.InvalidTokenError as e:
        return jsonify({
            "error": "invalid_token",
            "detail": str(e)
        }), 401

    scope_string = payload.get("scope", "")
    scopes = scope_string.split()

    if "write:admin" not in scopes:
        return jsonify({
            "error": "insufficient_scope",
            "required_scope": "write:admin",
            "token_scope": scope_string
        }), 403

    return jsonify({
        "message": "Admin action authorised",
        "scope": scope_string,
        "authenticated_client": payload.get("azp")
    }), 200
if __name__ == "__main__":
    app.run(port=5000, debug=False)
