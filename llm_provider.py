"""
SecureNova LLM provider abstraction.

Default: Ollama local inference.
Optional: Gemini REST API.

Environment:
  SECURENOVA_LLM=ollama|gemini
  SECURENOVA_OLLAMA_URL=http://127.0.0.1:11434
  SECURENOVA_OLLAMA_MODEL=llama3.2:3b
  GEMINI_API_KEY=...
  SECURENOVA_GEMINI_MODEL=gemini-2.5-flash
"""
import os
import time
import requests

PROVIDER = os.getenv("SECURENOVA_LLM", "ollama").lower()
OLLAMA_URL = os.getenv("SECURENOVA_OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("SECURENOVA_OLLAMA_MODEL", "llama3.2:3b")
GEMINI_MODEL = os.getenv("SECURENOVA_GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

def ollama_call(system_prompt, user_prompt, timeout=180):
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "options": {"temperature": 0.0},
        },
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["message"]["content"]

def gemini_call(system_prompt, user_prompt, timeout=60, retries=4):
    if not GEMINI_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set.")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent"
    )
    last = None
    for attempt in range(retries):
        r = requests.post(
            url,
            headers={"Content-Type": "application/json", "x-goog-api-key": GEMINI_KEY},
            json={
                "system_instruction": {"parts": [{"text": system_prompt}]},
                "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            },
            timeout=timeout,
        )
        if r.status_code == 429:
            last = r
            time.sleep(min(2 ** attempt, 12))
            continue
        r.raise_for_status()
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    last.raise_for_status()

def call_llm(system_prompt, user_prompt):
    if PROVIDER == "ollama":
        return ollama_call(system_prompt, user_prompt)
    if PROVIDER == "gemini":
        return gemini_call(system_prompt, user_prompt)
    raise ValueError("SECURENOVA_LLM must be 'ollama' or 'gemini'.")

def provider_status():
    return {
        "provider": PROVIDER,
        "ollama_url": OLLAMA_URL,
        "ollama_model": OLLAMA_MODEL,
        "gemini_model": GEMINI_MODEL,
    }
