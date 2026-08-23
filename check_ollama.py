import os, requests

url=os.getenv("SECURENOVA_OLLAMA_URL","http://127.0.0.1:11434")
model=os.getenv("SECURENOVA_OLLAMA_MODEL","llama3.2:3b")

print("Ollama URL:",url)
print("Model:",model)

r=requests.get(f"{url}/api/tags",timeout=10)
r.raise_for_status()
models=[m["name"] for m in r.json().get("models",[])]
print("Installed models:",models)

if model not in models:
    print(f"MODEL NOT FOUND: run `ollama pull {model}`")
    raise SystemExit(2)

r=requests.post(
    f"{url}/api/chat",
    json={"model":model,"stream":False,
          "messages":[{"role":"user","content":"Respond exactly: SecureNova Ollama connection successful"}]},
    timeout=120,
)
r.raise_for_status()
print(r.json()["message"]["content"])
print("Ollama connection: OK")
