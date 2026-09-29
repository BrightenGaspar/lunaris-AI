import os
import shutil
import uuid
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Security, Depends, UploadFile, File, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from lunaris_core import LunarisEngine
from rag_ingest import DocumentIngestionEngine
from sandbox import CodeExecutionSandbox
from voice_engine import LunarisVoiceEngine

API_SECRET_TOKEN = os.getenv("LUNARIS_API_KEY", "lunaris_dev_token")
DOCUMENTS_DIR = Path(os.getenv("LUNARIS_DOCUMENTS_DIR", "./documents"))
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
VOICE_CACHE = Path(os.getenv("LUNARIS_VOICE_DIR", "./voice_cache"))
VOICE_CACHE.mkdir(parents=True, exist_ok=True)

security = HTTPBearer(auto_error=False)

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if os.getenv("LUNARIS_AUTH_DISABLED", "true").lower() == "true":
        return True
    if credentials and credentials.credentials == API_SECRET_TOKEN:
        return True
    raise HTTPException(status_code=401, detail="Unauthorized: Invalid or missing API token")

app = FastAPI(
    title="🌕 Lunaris AI Sovereign Platform Gateway",
    version="2.2.0",
    description="Sovereign AI API with ReAct Agent reasoning, Multi-format RAG, Air-gapped Voice, and Sandboxed Code Execution."
)

# Enable CORS for Next.js and frontend web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = LunarisEngine()
ingest_engine = DocumentIngestionEngine()
sandbox = CodeExecutionSandbox()
voice_engine = LunarisVoiceEngine()

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

class VoiceSynthesisRequest(BaseModel):
    text: str

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
        result = engine.run_react_agent(user_query=req.prompt, session_id=req.session_id)
        return {"session_id": result["session_id"], "response": result["response"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Document Management
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

# Voice Endpoints
@app.post("/api/v1/voice/transcribe", dependencies=[Depends(verify_token)])
async def voice_transcribe_endpoint(file: UploadFile = File(...)):
    """
    Transcribes uploaded audio to text using local Whisper.
    """
    temp_path = VOICE_CACHE / f"temp_{uuid.uuid4().hex}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = voice_engine.transcribe_audio(str(temp_path))
    if temp_path.exists():
        temp_path.unlink()

    return {"transcription": text}

@app.post("/api/v1/voice/synthesize", dependencies=[Depends(verify_token)])
async def voice_synthesize_endpoint(req: VoiceSynthesisRequest):
    """
    Synthesizes text into offline speech WAV audio.
    """
    out_file = voice_engine.synthesize_speech(req.text)
    if not out_file or not os.path.exists(out_file):
        raise HTTPException(status_code=500, detail="Speech synthesis failed.")
    return FileResponse(out_file, media_type="audio/wav", filename="speech.wav")

@app.post("/api/v1/voice/chat", dependencies=[Depends(verify_token)])
async def voice_chat_endpoint(file: UploadFile = File(...), session_id: Optional[str] = Form(None)):
    """
    End-to-end voice query processing: Audio Input -> Transcribe -> ReAct Agent -> Synthesize -> Audio Output.
    """
    temp_path = VOICE_CACHE / f"temp_{uuid.uuid4().hex}_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcribed_text = voice_engine.transcribe_audio(str(temp_path))
    if temp_path.exists():
        temp_path.unlink()

    result = engine.run_react_agent(user_query=transcribed_text, session_id=session_id)
    speech_wav = voice_engine.synthesize_speech(result["response"])

    return {
        "transcription": transcribed_text,
        "response": result["response"],
        "session_id": result["session_id"],
        "audio_url": f"/api/v1/voice/download/{Path(speech_wav).name}" if speech_wav else None
    }

@app.get("/api/v1/voice/download/{filename}")
async def download_audio(filename: str):
    file_path = VOICE_CACHE / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    return FileResponse(str(file_path), media_type="audio/wav")

# Code Sandbox
@app.post("/api/v1/sandbox/execute", dependencies=[Depends(verify_token)])
async def execute_code_endpoint(req: CodeRequest):
    """
    Runs untrusted Python code inside the air-gapped Docker sandbox.
    """
    return sandbox.execute_python(req.code)

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "online",
        "mode": "air-gapped-sovereign",
        "version": "2.2.0",
        "voice": "enabled",
        "rag": "active",
        "agent": "ReAct-Autonomous-V2"
    }
