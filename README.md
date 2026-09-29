# 🌕 Lunaris AI — Sovereign Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-black.svg)](https://ollama.com/)
[![pgvector](https://img.shields.io/badge/pgvector-PostgreSQL-336791.svg?logo=postgresql)](https://github.com/pgvector/pgvector)

**Lunaris AI** is a fully sovereign, self-hosted, private intelligence platform designed with zero external cloud dependencies. It unifies local Large Language Models (LLMs), high-speed vector retrieval with `pgvector`, autonomous ReAct multi-step tool reasoning, live document folder monitoring, private internet metasearch with SearXNG, and ephemeral sandboxed code execution.

---

## 🏗️ Architecture

```mermaid
graph TD
    Client["Client Interface (OpenWebUI / FastAPI Swagger / Custom App)"] --> Gateway["FastAPI Gateway (main.py)"]
    Gateway --> Auth["Bearer Token Auth Guardrail"]
    Gateway --> ReActAgent["Autonomous ReAct Agent (lunaris_core.py)"]
    
    subgraph ReAct Loop (Thought -> Action -> Observation)
        ReActAgent -->|1. Vector Search| ToolDoc["search_documents (pgvector)"]
        ReActAgent -->|2. Web Metasearch| ToolWeb["web_search (SearXNG)"]
        ReActAgent -->|3. Sandboxed Eval| ToolCode["execute_python_sandbox (Docker)"]
        ReActAgent -->|4. Arithmetic| ToolMath["calculate_math"]
        ReActAgent -->|5. Memory / Stats| ToolList["list_knowledge_base"]
    end

    subgraph Document Ingestion Pipeline
        Watcher["Live Folder Watcher (watcher.py)"] -->|Watches ./documents/| Ingest["Multi-Format Parser (rag_ingest.py)"]
        Ingest -->|PDF, DOCX, CSV, MD, Code| Chunker["Semantic Chunker"]
        Chunker -->|Vector Embeddings| Ollama["Ollama (nomic-embed-text)"]
        Chunker -->|HNSW Cosine Index| Postgres["PostgreSQL 16 + pgvector"]
    end
```

---

## 🚀 Key Features

- **🛡️ 100% Data Sovereignty**: All inference, embedding, and vector storage run locally on your hardware.
- **🤖 Autonomous ReAct Reasoning**: Multi-step Thought $\rightarrow$ Action $\rightarrow$ Observation reasoning loop capable of using multiple tools in sequence.
- **📂 Multi-Format Ingestion Engine**: Native parsing and chunking for **PDF, DOCX, CSV, JSON, Markdown, Text, and source code files**.
- **👁️ Live Folder Watcher**: Background daemon that continuously watches `./documents/`, automatically detecting additions, modifications, and deletions.
- **⚡ Local Vector RAG**: Fast Approximate Nearest Neighbor search using PostgreSQL `pgvector` with HNSW cosine distance indexing and SHA-256 deduplication.
- **🔍 Privacy-Preserving Metasearch**: Real-time web groundings via self-hosted SearXNG without user tracking.
- **🔒 Air-Gapped Code Sandbox**: Resource-capped, non-networked Docker container execution for untrusted Python code.
- **🔑 Production API Gateway**: Token-authenticated REST API with OpenAPI documentation and multipart document uploads.

---

## 📂 Repository Structure

```
lunaris-ai/
├── documents/             # Drop zone for auto-ingested documents (PDF, DOCX, CSV, MD, Code)
│   ├── sample_architecture.md
│   ├── company_metrics.csv
│   └── sample_python_code.py
├── docker-compose.yml     # Complete container stack (Ollama, pgvector, SearXNG, OpenWebUI)
├── init.sql               # Database schema with pgvector & conversation memory
├── lunaris_core.py        # Central Autonomous ReAct reasoning engine
├── agent_tools.py         # Registry of agent tools (vector search, web search, sandbox, math)
├── sandbox.py             # Docker-based isolated code execution sandbox
├── rag_ingest.py          # Multi-format document parser & vector ingestion pipeline
├── watcher.py             # Live folder watcher daemon for real-time document indexing
├── main.py                # FastAPI production REST gateway
├── requirements.txt       # Python dependencies
├── .env.example           # Environment configuration template
└── README.md              # Project documentation
```

---

## ⚡ Getting Started

### 1. Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Python 3.10+](https://www.python.org/)
- *(Optional)* NVIDIA GPU with CUDA support for accelerated local inference.

### 2. Clone and Setup Environment
```bash
git clone https://github.com/BrightenGaspar/Lunaris-AI.git
cd Lunaris-AI
cp .env.example .env
```

### 3. Launch Docker Services
```bash
docker compose up -d
```

### 4. Pull Local AI Models
```bash
# Pull conversation LLM
docker exec -it lunaris_ollama ollama pull llama3.3

# Pull embedding model for RAG
docker exec -it lunaris_ollama ollama pull nomic-embed-text
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run Ingestion / Watcher
```bash
# Option A: Ingest all files in ./documents/ once
python rag_ingest.py

# Option B: Run live folder watcher daemon
python watcher.py
```

### 7. Start the Lunaris Gateway
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 Service Endpoints

| Service | URL | Description |
| :--- | :--- | :--- |
| **OpenWebUI** | `http://localhost:3000` | Interactive Chat Web Interface |
| **FastAPI Swagger Docs** | `http://localhost:8000/docs` | Interactive REST API Documentation |
| **SearXNG Search** | `http://localhost:8080` | Local Private Metasearch Engine |
| **Ollama API** | `http://localhost:11434` | Raw Local LLM Inference Engine |

---

## 📡 API Reference

### 1. Autonomous ReAct Reasoning
`POST /api/v1/agent/react`
```json
{
  "prompt": "Look up our Q1 cost savings in company_metrics.csv and calculate the square root of that amount.",
  "session_id": "optional-uuid-string",
  "max_iterations": 5
}
```

*Response includes complete step-by-step reasoning:*
```json
{
  "session_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
  "query": "Look up our Q1 cost savings...",
  "response": "The Q1 cost savings for Engineering was $45,000, and the square root is approximately 212.13.",
  "reasoning_steps": [
    {
      "step": 1,
      "action": "search_documents",
      "action_input": "Q1 cost saved company metrics",
      "observation": "[1] Source: 'company_metrics' ... CostSavedUSD: 45000"
    },
    {
      "step": 2,
      "action": "calculate_math",
      "action_input": "sqrt(45000)",
      "observation": "Result: 212.13203435596424"
    }
  ],
  "total_steps": 2
}
```

### 2. Direct Multipart Document Upload
`POST /api/v1/documents/upload`
Uploads and indexes any PDF, DOCX, CSV, TXT, or Code file immediately.

### 3. List All Indexed Documents
`GET /api/v1/documents/list`

### 4. Sandboxed Code Execution
`POST /api/v1/sandbox/execute`
```json
{
  "code": "import math\nprint(f'Calculated: {math.sqrt(256)}')"
}
```

---

## 📄 License
This project is licensed under the MIT License.
