# AI Cloud Operations Agent

An AI-powered cloud operations agent that converts natural language queries into **safe, deterministic AWS actions**.  
The system uses a **capability-driven architecture** with optional **local LLM + RAG** support to avoid hallucinations and ensure production correctness.

---

## 🚀 Features

- 🔎 Query AWS resources using **natural language**
- 🧠 Deterministic intent + entity extraction (no blind LLM execution)
- ☁️ AWS integrations (CodePipeline, ecs , s3 — extensible)
- 📦 Local **LLM (Ollama)** with **RAG (ChromaDB)** for grounded responses
- 🐳 Fully **Dockerized** stack (UI, backend, LLM, vector DB)
- 💬 Chat-style **React UI**
- 🔐 Read-only, safe-by-design architecture

---

## 🧠 How It Works (High Level)

User Query
↓
Intent Detection (capability-based)
↓
Entity Extraction (pipeline, bucket, region, etc.)
↓
AWS SDK (boto3) – source of truth
↓
Canonical JSON response
↓
(Optional) LLM summary using RAG


> **Key principle:**  
> *Language is flexible. Capabilities are finite.*  
> The LLM never decides permissions or executes AWS actions.

---

## 🔧 Supported Capabilities (Current)

### AWS CodePipeline
- Pipeline status (Succeeded / Failed / InProgress)
- Last execution time
- Commit ID that triggered the pipeline
- Connected GitHub repository & branch
- Correct handling of failed stages (matches AWS Console)

Example prompt:


---

## ▶️ Running Locally

### Prerequisites
- Docker
- Docker Compose
- AWS credentials (read-only recommended)

---

### 1️⃣ Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

2️⃣ Set environment variables
environment:
  AWS_REGION=eu-west-2
  AWS_DEFAULT_REGION=eu-west-2
  AWS_ACCESS_KEY_ID=xxxx
  AWS_SECRET_ACCESS_KEY=xxxx
  AWS_SESSION_TOKEN=xxxx   # if applicable


3️⃣ Start the stack
docker compose up -d --build


4️⃣ Access the app

UI: http://localhost:3000

Backend API: http://localhost:8080

ChromaDB: http://localhost:8001

Ollama: http://localhost:11434