import json
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

OUT=Path(__file__).resolve().parent/"evidence"
OUT.mkdir(exist_ok=True)

def canonical(message):
    return json.dumps(message,sort_keys=True,separators=(",",":")).encode()

def generate():
    private=Ed25519PrivateKey.generate()
    public=private.public_key()
    private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption())
    (OUT/"agent_a_private_key.pem").write_bytes(
        private.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    (OUT/"agent_a_public_key.pem").write_bytes(
        public.public_bytes(serialization.Encoding.PEM,serialization.PublicFormat.SubjectPublicKeyInfo))
    return private,public

def sign(private,message):
    return {"message":message,"signature":private.sign(canonical(message)).hex()}

def verify(public,envelope):
    try:
        public.verify(bytes.fromhex(envelope["signature"]),canonical(envelope["message"]))
        print("SIGNATURE VALID — processing message")
        return True
    except InvalidSignature:
        print("SIGNATURE INVALID — REJECTING message")
        return False

if __name__=="__main__":
    private,public=generate()
    msg={"sender":"agent_a_orchestrator","instruction":"approve_refund(amount=1000)",
         "timestamp":datetime.now(timezone.utc).isoformat()}
    env=sign(private,msg)
    print("Generated agent_a_private_key.pem and agent_a_public_key.pem")
    verify(public,env)
    tampered=json.loads(json.dumps(env))
    tampered["message"]["instruction"]="approve_refund(amount=9000)"
    print("Tampering instruction from 1000 to 9000")
    assert verify(public,tampered) is False
    fake={"message":{"sender":"agent_a_orchestrator","instruction":"grant_admin_access(attacker)"},
          "signature":"00"*64}
    print("Spoofed unsigned message")
    assert verify(public,fake) is False
