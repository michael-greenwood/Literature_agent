# llm_client.py
import requests

OLLAMA_URL = "http://132.156.103.65:11434/api/generate"
MODEL = "llama3.1:8b"

def query_llm(prompt: str, timeout_s: int = 90) -> str:
    r = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=timeout_s
    )
    r.raise_for_status()
    return r.json()["response"]
