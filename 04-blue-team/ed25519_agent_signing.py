"""
Project 4 cryptographic agent identity binding.

Generates Ed25519 keys, signs every outgoing message, verifies on receipt,
and demonstrates rejection of a one-character tamper.
"""
from pathlib import Path
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / "evidence" / "agent_a_private_key.pem"
PUBLIC = HERE / "evidence" / "agent_a_public_key.pem"

def generate_keys():
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    PRIVATE.write_bytes(private.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ))
    PUBLIC.write_bytes(public.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo
    ))
    return private, public

def sign_message(private, message: str):
    return base64.b64encode(private.sign(message.encode())).decode()

def verify_message(public, message: str, signature_b64: str):
    from cryptography.exceptions import InvalidSignature
    try:
        public.verify(base64.b64decode(signature_b64), message.encode())
        return True, "SIGNATURE VERIFIED"
    except InvalidSignature:
        return False, "SIGNATURE VERIFICATION FAILED: tampered message rejected"

def main():
    private, public = generate_keys()
    message = "Agent-A -> Agent-B | action=read:ai-data | nonce=MSG-001"
    sig = sign_message(private, message)

    ok, log = verify_message(public, message, sig)
    print(log)

    tampered = message.replace("read:ai-data", "write:admin")
    ok2, log2 = verify_message(public, tampered, sig)
    print(log2)
    if ok2:
        raise SystemExit("ERROR: tampered message was accepted")

    print(f"Private key: {PRIVATE}")
    print(f"Public key : {PUBLIC}")

if __name__ == "__main__":
    main()
