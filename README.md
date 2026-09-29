# 🌕 Lunaris AI — Sovereign Intelligence Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-black.svg?logo=flask)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth_OTP-3ECF8E.svg?logo=supabase)](https://supabase.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg?logo=next.js)](https://nextjs.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker)](https://www.docker.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Local_Inference-black.svg)](https://ollama.com/)
[![pgvector](https://img.shields.io/badge/pgvector-PostgreSQL-336791.svg?logo=postgresql)](https://github.com/pgvector/pgvector)

**Lunaris AI** is a sovereign, self-hosted, private intelligence platform designed with zero external cloud dependencies. It unifies local Large Language Models (LLMs), high-speed vector retrieval with `pgvector`, autonomous ReAct multi-step tool reasoning, live document folder monitoring, air-gapped voice interaction (Whisper + TTS), Telegram & Discord connectors, and a secure Supabase Email OTP authentication portal.

---

## 🏗️ Architecture

```mermaid
graph TD
    User["User Client"] --> AuthPortal["Flask + Supabase Auth Portal (auth_app.py)"]
    AuthPortal -->|Email OTP Verification| Supabase["Supabase Auth Service"]
    AuthPortal -->|Authenticated Access| NextApp["Next.js Web Dashboard (Port 3001)"]
    
    NextApp --> Gateway["FastAPI Gateway (main.py)"]
    Gateway --> ReActAgent["Autonomous ReAct Agent (lunaris_core.py)"]
    
    subgraph ReAct Tool Execution Loop
        ReActAgent -->|1. Vector Search| ToolDoc["search_documents (pgvector)"]
        ReActAgent -->|2. Web Metasearch| ToolWeb["web_search (SearXNG)"]
        ReActAgent -->|3. Sandboxed Eval| ToolCode["execute_python_sandbox (Docker)"]
        ReActAgent -->|4. Arithmetic| ToolMath["calculate_math"]
        ReActAgent -->|5. Catalog Inspection| ToolList["list_knowledge_base"]
    end

    subgraph Sovereign Pipelines
        Watcher["Live Watcher (watcher.py)"] -->|Watches ./documents/| Ingest["Multi-Format Parser (rag_ingest.py)"]
        Ingest -->|PDF, DOCX, CSV, MD, Code| Chunker["Semantic Chunker + SHA256"]
        Chunker -->|Dense Vector Embeddings| Ollama["Ollama (nomic-embed-text)"]
        Chunker -->|HNSW Cosine Index| Postgres["PostgreSQL 16 + pgvector"]
        Voice["Voice Engine (voice_engine.py)"] -->|STT| Whisper["Local Whisper"]
        Voice -->|TTS| Piper["Local Speech TTS"]
    end
```

---

## 🚀 Complete Feature Set

- **🛡️ 100% Data Sovereignty**: All inference, embedding, voice, and vector storage run offline on your hardware.
- **🔐 Supabase Email OTP Auth**: Secure passwordless login portal with custom planet glassmorphism UI.
- **🎨 Dedicated Next.js Web App**: Dark celestial dashboard with real-time reasoning trace accordions, document manager, sandbox terminal, and voice mic.
- **🤖 Autonomous ReAct Reasoning**: Multi-step Thought $\rightarrow$ Action $\rightarrow$ Observation reasoning loop capable of chaining multiple tools in sequence.
- **🎙️ Air-Gapped Voice (STT & TTS)**: Talk to Lunaris via microphone and receive natural synthesized speech responses offline.
- **💬 Telegram & Discord Bots**: Interact with your sovereign AI from your smartphone or team chat with voice note and document upload support.
- **📂 Multi-Format Ingestion**: Native parsing and chunking for **PDF, DOCX, CSV, JSON, Markdown, Text, and source code files**.
- **👁️ Live Folder Watcher**: Background daemon monitoring `./documents/` for instant vector indexing and automatic deletion syncing.
- **⚡ Fast Vector RAG**: PostgreSQL `pgvector` with HNSW cosine distance indexing and SHA-256 deduplication.
- **🔒 Air-Gapped Code Sandbox**: Resource-capped, non-networked Docker container execution for untrusted Python code.

---

## 📂 Repository Structure

```
lunaris-ai/
├── auth_app.py            # Flask + Supabase Email OTP authentication portal
├── supabase_email_template.html # Supabase Email OTP customization template
├── frontend/              # Dedicated Next.js & Tailwind CSS Web Application
├── documents/             # Drop zone for auto-ingested documents (PDF, DOCX, CSV, MD, Code)
├── docker-compose.yml     # Container stack (Ollama, pgvector, SearXNG, OpenWebUI)
├── init.sql               # Database schema with pgvector & conversation memory
├── lunaris_core.py        # Central Autonomous ReAct reasoning engine
├── agent_tools.py         # Registry of agent tools (vector search, web search, sandbox, math)
├── sandbox.py             # Docker-based isolated code execution sandbox
├── rag_ingest.py          # Multi-format document parser & vector ingestion pipeline
├── watcher.py             # Live folder watcher daemon for real-time document indexing
├── voice_engine.py        # Air-gapped Speech-to-Text & Text-to-Speech engine
├── telegram_bot.py        # Telegram bot connector with voice and document support
├── discord_bot.py         # Discord bot connector with attachment parsing
├── main.py                # FastAPI production REST gateway
├── requirements.txt       # Python dependencies
├── .env.example           # Environment configuration template
└── README.md              # Project documentation
```

---

## ⚡ Getting Started

### 1. Setup Environment
```bash
git clone https://github.com/BrightenGaspar/Lunaris-AI.git
cd Lunaris-AI
cp .env.example .env
```

### 2. Launch Docker Services
```bash
docker compose up -d
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Services

**Start Supabase Auth Portal:**
```bash
python auth_app.py
# Access at http://127.0.0.1:5000
```

**Start FastAPI Gateway:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Start Next.js Frontend:**
```bash
cd frontend
npm install
npm run dev
# Access at http://localhost:3001
```

---

## 📄 License
This project is licensed under the MIT License.
