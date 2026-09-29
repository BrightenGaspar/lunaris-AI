import os
import shutil
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Security, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from lunaris_core import LunarisEngine
from rag_ingest import DocumentIngestionEngine
from sandbox import CodeExecutionSandbox

API_SECRET_TOKEN = os.getenv("LUNARIS_API_KEY", "lunaris_dev_token")
DOCUMENTS_DIR = Path(os.getenv("LUNARIS_DOCUMENTS_DIR", "./documents"))
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if os.getenv("LUNARIS_AUTH_DISABLED", "false").lower() == "true":
        return True
    if credentials and credentials.credentials == API_SECRET_TOKEN:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API token")

app = FastAPI(
    title="🌕 Lunaris AI Sovereign Platform Gateway",
    version="2.1.0",
    description="Sovereign AI API supporting ReAct Agent reasoning, Multi-format RAG, Sandboxed Code Execution, and Document Ingestion."
)

engine = LunarisEngine()
ingest_engine = DocumentIngestionEngine()
sandbox = CodeExecutionSandbox()

# Request Schemas
class ReActAgentRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    max_iterations: int = 5

class ChatRequest(BaseModel):
    prompt: str
    session_id: Optional[str] = None
    use_web: bool = False
    use_docs: bool = False

class CodeRequest(BaseModel):
    code: str

# Endpoints
@app.post("/api/v1/agent/react", dependencies=[Depends(verify_token)])
async def react_agent_endpoint(req: ReActAgentRequest):
    """
    Executes the multi-step Autonomous ReAct reasoning loop.
    Returns the final answer along with step-by-step thoughts, actions, and observations.
    """
    try:
        result = engine.run_react_agent(
            user_query=req.prompt,
            session_id=req.session_id,
            max_iterations=req.max_iterations
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/chat", dependencies=[Depends(verify_token)])
async def chat_endpoint(req: ChatRequest):
    """
    Standard chat inference endpoint with conversation memory.
    """
    try:
        # Default to the ReAct agent for comprehensive tool handling
        result = engine.run_react_agent(user_query=req.prompt, session_id=req.session_id)
        return {"session_id": result["session_id"], "response": result["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/documents/upload", dependencies=[Depends(verify_token)])
async def upload_document_endpoint(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None)
):
    """
    Uploads a document (PDF, DOCX, CSV, TXT, MD, Code), saves it to ./documents/, and indexes it into pgvector.
    """
    try:
        dest_path = DOCUMENTS_DIR / file.filename
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        doc_title = title or dest_path.stem
        res = ingest_engine.ingest_file(str(dest_path), title=doc_title, force_reindex=True)
        return {
            "status": "success",
            "file_name": file.filename,
            "details": res
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload and ingest document: {e}")

@app.get("/api/v1/documents/list", dependencies=[Depends(verify_token)])
async def list_documents_endpoint():
    """
    Returns all documents currently indexed in pgvector with chunk statistics.
    """
    try:
        docs = ingest_engine.list_indexed_documents()
        return {"total_documents": len(docs), "documents": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/documents/{title}", dependencies=[Depends(verify_token)])
async def delete_document_endpoint(title: str):
    """
    Deletes a document and all its vector embeddings from the database.
    """
    try:
        deleted = ingest_engine.delete_document_by_path_or_title(title)
        return {"status": "success", "message": f"Deleted {deleted} chunks for '{title}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sandbox/execute", dependencies=[Depends(verify_token)])
async def execute_code_endpoint(req: CodeRequest):
    """
    Runs untrusted Python code inside the air-gapped Docker sandbox.
    """
    return sandbox.execute_python(req.code)

@app.get("/api/v1/health")
async def health_check():
    """
    Health check endpoint for container liveness and readiness probes.
    """
    return {
        "status": "online",
        "mode": "air-gapped-sovereign",
        "version": "2.1.0",
        "agent": "ReAct-Autonomous-V2"
    }
