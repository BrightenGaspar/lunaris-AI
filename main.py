import os
import uuid
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from lunaris_core import LunarisEngine
from rag_ingest import ingest_file

API_SECRET_TOKEN = os.getenv("LUNARIS_API_KEY", "lunaris_dev_token")
security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if os.getenv("LUNARIS_AUTH_DISABLED", "false").lower() == "true":
        return True
    if credentials and credentials.credentials == API_SECRET_TOKEN:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API token")

app = FastAPI(
    title="Lunaris AI Platform Gateway",
    version="2.0.0",
    description="Sovereign AI Gateway for Local LLMs, pgvector RAG, SearXNG, and Sandbox Execution."
)

engine = LunarisEngine()

class ChatRequest(BaseModel):
    prompt: str
    session_id: str | None = None
    use_web: bool = False
    use_docs: bool = False

class CodeRequest(BaseModel):
    code: str

class IngestRequest(BaseModel):
    file_path: str
    title: str

@app.post("/api/v1/chat", dependencies=[Depends(verify_token)])
async def chat_endpoint(req: ChatRequest):
    try:
        session_id = req.session_id or str(uuid.uuid4())
        response = engine.run_agent(
            user_query=req.prompt,
            session_id=session_id,
            use_web=req.use_web,
            use_docs=req.use_docs
        )
        return {"session_id": session_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/sandbox/execute", dependencies=[Depends(verify_token)])
async def execute_code_endpoint(req: CodeRequest):
    return engine.execute_code(req.code)

@app.post("/api/v1/documents/ingest", dependencies=[Depends(verify_token)])
async def ingest_document_endpoint(req: IngestRequest):
    try:
        ingest_file(req.file_path, req.title)
        return {"status": "success", "message": f"Document '{req.title}' indexed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    return {"status": "online", "mode": "air-gapped-sovereign"}
