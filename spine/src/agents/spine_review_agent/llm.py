import requests

OLLAMA_URL = "http://132.156.103.65:11434/api/generate"
MODEL = "llama3.1:8b"

def query_llm(prompt: str) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()["response"]
