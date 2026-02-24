# AI Cloud Operations Agent

An AI-powered cloud operations assistant designed to let you query and manage your AWS environments using **natural language**.  
Instead of navigating through dozens of AWS Console tabs, developers can chat directly with the agent to fetch pipeline statuses, check deployments, list S3 buckets, and even modify parameter store variables.

This agent operates using a **LangChain ReAct Architecture** powered by a **local Ollama LLM**, ensuring that no sensitive AWS metadata is sent to third-party APIs.

---

## 🚀 Key Features

- 💬 **Natural Language Interface**: Query your AWS infrastructure using plain English.
- 🐳 **Fully Dockerized Stack**: Backend, Frontend, VectorDB, and Local LLM run out-of-the-box.
- 🧠 **LangChain ReAct Agent**: Intelligently decides which AWS tools to use to get the job done.
- 🔐 **Cross-Account Support**: Switch AWS environments (Dev, Staging, Prod) seamlessly via the UI dropdown. The backend dynamically uses `sts:AssumeRole` to securely query other accounts.
- 📦 **100% Local Processing**: Uses `Ollama` hosting the `Mistral` model locally, ensuring total privacy.

---

## 🔧 Supported Capabilities

The AI currently has programmatic access to query the following services via Boto3:

*   **S3**: List buckets
*   **EC2**: Describe running and stopped instances (can filter by name/state)
*   **ECS**: Fetch specific cluster and service deployment statuses (Running/Pending/Desired tasks)
*   **EKS**: List EKS clusters and fetch detailed endpoint/version status
*   **CodePipeline**: Get latest execution status, pipeline stage details, last commit ID, and Github branch triggers
*   **SSM Parameter Store**: Fetch, list, and update environment variables, with built-in safety blocks for production endpoints.

---

## 🏗️ Architecture

1.  **React Frontend (Vite)**: A sleek, modern chat interface with a built-in cross-account selector dropdown.
2.  **FastAPI Backend**: Handles traffic routing, context management, and AWS authentication (Boto3).
3.  **LangChain Agent Core**: The brain of the operation. Holds a toolkit of Python Boto3 functions and iteratively reasons with the LLM to get answers.
4.  **Local LLM (Ollama)**: Houses the local AI model.
5.  **ChromaDB**: (Vector Store) Available for RAG integration over your internal engineering runbooks.

---

## ▶️ Running Locally

### Prerequisites
- Docker & Docker Compose
- AWS Access Keys with sufficient IAM permissions to read from the services listed above.

### 1️⃣ Clone the repo
```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 2️⃣ Configure AWS Credentials
Open `docker-compose.yml` and insert your AWS credentials for the `backend` service:

```yaml
    environment:
      - AWS_REGION=eu-west-2
      - AWS_DEFAULT_REGION=eu-west-2
      - AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
      - AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
      - AWS_SESSION_TOKEN=YOUR_SESSION_TOKEN # If using SSO 
```

### 3️⃣ Start the Stack
Boot up the entire environment. Keep in mind that pulling the LLM image may take a few minutes on the first run.
```bash
docker compose up -d --build
```

### 4️⃣ Access the App

*   **UI Dashboard & Chat**: [http://localhost:3000](http://localhost:3000)
*   **Backend API**: [http://localhost:8080](http://localhost:8080)
*   **ChromaDB**: [http://localhost:8001](http://localhost:8001)
*   **Ollama Endpoint**: [http://localhost:11434](http://localhost:11434)