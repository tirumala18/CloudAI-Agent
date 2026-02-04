from app.rag import rag_search
from app.llm import ask_llm
import json
import re

ALLOWED_COMMANDS = ["list-s3", "describe-ec2","codepipeline-status"]

def interpret_command(user_query: str) -> str:
    q = user_query.lower()

    # ---------- LAYER 1: deterministic guard ----------
    if "s3" in q and ("list" in q or "bucket" in q):
        return "list-s3"

    if "ec2" in q and ("describe" in q or "list" in q or "instance" in q):
        return "describe-ec2"
    
    if "pipeline" in q:
        return "codepipeline-status"


    # ---------- LAYER 2: LLM + RAG ----------
    docs = rag_search(user_query)

    prompt = f"""
You are an AWS automation agent.

Based on the documentation below, decide the AWS command.

Documentation:
{docs}

User request:
"{user_query}"

Return ONLY JSON in this format:
{{ "command": "list-s3" | "describe-ec2" }}

No explanation.
"""

    raw = ask_llm(prompt)

    # ---------- HARD PARSE ----------
    try:
        data = json.loads(raw)
        cmd = data.get("command", "")
    except Exception:
        match = re.search(r"(list-s3|describe-ec2)", raw.lower())
        cmd = match.group(1) if match else "unknown"

    return cmd if cmd in ALLOWED_COMMANDS else "unknown"
