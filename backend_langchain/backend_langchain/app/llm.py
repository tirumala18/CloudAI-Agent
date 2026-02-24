from langchain_ollama import OllamaLLM
import os

LLM_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://llm:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "mistral")

# Single shared LLM instance
llm = OllamaLLM(
    base_url=LLM_BASE_URL,
    model=MODEL_NAME,
    temperature=0,        # deterministic — important for tool selection
)
