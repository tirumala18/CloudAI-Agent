import requests
import os

LLM_URL = os.getenv("LLM_URL")

def ask_llm(prompt: str):
    payload = {
        "model": "mistral",
        "prompt": prompt
    }
    response = requests.post(LLM_URL, json=payload, stream=False)
    return response.text.strip()
