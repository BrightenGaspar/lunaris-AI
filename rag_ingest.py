import os
import sys
import csv
import json
import hashlib
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Any, Optional
import requests
import psycopg2
from psycopg2.extras import Json, RealDictCursor

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lunaris_ai"),
    "user": os.getenv("DB_USER", "lunaris"),
    "password": os.getenv("DB_PASSWORD", "lunaris_secure_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".markdown", ".json", ".csv", ".pdf", ".docx",
    ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css", ".sql",
    ".c", ".cpp", ".h", ".hpp", ".java", ".go", ".rs", ".yaml", ".yml",
    ".sh", ".bash", ".ps1"
}

def calculate_file_hash(file_path: str) -> str:
    """Computes SHA-256 hash of a file for change detection and deduplication."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()

def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from PDF files using pypdf if available, with built-in fallback."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        pages_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages_text.append(f"--- Page {i + 1} ---\n{text}")
        return "\n\n".join(pages_text)
    except ImportError:
        # Simple fallback for text extraction if pypdf is not yet installed
        print("[Notice] pypdf not installed. Reading binary stream...")
        with open(file_path, "rb") as f:
            raw = f.read()
        # Basic text stream extraction from PDF bytes
        import re
        text_matches = re.findall(rb"\(([\w\s\.\,\;\:\-\?!]+)\)\s*Tj", raw)
        if text_matches:
            return " ".join([m.decode("latin-1", errors="ignore") for m in text_matches])
        return f"[PDF Binary File: {os.path.basename(file_path)}. Install 'pypdf' for full extraction]"

def extract_text_from_docx(file_path: str) -> str:
    """Extracts text from DOCX files using python-docx or native XML zip parsing."""
    try:
        import docx
        doc = docx.Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    except ImportError:
        # Native DOCX extraction (DOCX is a zip containing word/document.xml)
        try:
            with zipfile.ZipFile(file_path) as docx_zip:
                xml_content = docx_zip.read('word/document.xml')
                tree = ET.fromstring(xml_content)
                namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
                texts = []
                for p in tree.iterfind('.//w:p', namespaces):
                    p_text = ''.join(node.text for node in p.iterfind('.//w:t', namespaces) if node.text)
                    if p_text.strip():
                        texts.append(p_text)
                return "\n".join(texts)
        except Exception as e:
            return f"[Error parsing DOCX: {e}]"

def extract_text_from_csv(file_path: str) -> str:
    """Converts CSV rows into clean readable structured text lines."""
    rows = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        if headers:
            rows.append(f"Headers: {', '.join(headers)}")
            for i, row in enumerate(reader):
                if i > 500: # Limit single CSV snippet
                    rows.append("... [Additional rows truncated]")
                    break
                row_str = " | ".join([f"{h}: {val}" for h, val in zip(headers, row) if val.strip()])
                if row_str:
                    rows.append(f"Row {i+1}: {row_str}")
        else:
            return ""
    return "\n".join(rows)

def extract_text_from_json(file_path: str) -> str:
    """Extracts and formats JSON content."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        try:
            data = json.load(f)
            return json.dumps(data, indent=2)
        except Exception:
            f.seek(0)
            return f.read()

def extract_document_text(file_path: str) -> str:
    """Universal document text extractor supporting multiple file formats."""
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".csv":
        return extract_text_from_csv(file_path)
    elif ext == ".json":
        return extract_text_from_json(file_path)
    else:
        # Default plain text / markdown / code files
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    """Generates dense vector embeddings via local Ollama instance."""
    try:
        res = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": model, "prompt": text}, timeout=30)
        res.raise_for_status()
        return res.json().get("embedding", [])
    except Exception as e:
        print(f"[Embedding Error] Failed to generate embedding with {model}: {e}")
        return [0.0] * 768

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 60) -> List[str]:
    """
    Semantic sliding-window text chunker.
    Splits text by paragraphs/sentences while respecting word boundaries and chunk size.
    """
    if not text.strip():
        return []

    # First attempt to split on double newlines (paragraphs)
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_words = 0

    for para in paragraphs:
        para_words = para.split()
        if not para_words:
            continue

        if current_words + len(para_words) <= chunk_size:
            current_chunk.append(para)
            current_words += len(para_words)
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            
            # If a single paragraph is larger than chunk_size, split by word window
            if len(para_words) > chunk_size:
                step = max(1, chunk_size - overlap)
                for i in range(0, len(para_words), step):
                    sub_chunk = " ".join(para_words[i:i + chunk_size])
                    if sub_chunk.strip():
                        chunks.append(sub_chunk)
                current_chunk = []
                current_words = 0
            else:
                current_chunk = [para]
                current_words = len(para_words)

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks

class DocumentIngestionEngine:
    def __init__(self, embed_model: str = "nomic-embed-text"):
        self.embed_model = embed_model

    def get_db_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def is_file_indexed(self, file_hash: str) -> bool:
        """Checks if a file with the identical content hash is already present in pgvector."""
        conn = self.get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM lunaris_documents WHERE file_hash = %s", (file_hash,))
            count = cur.fetchone()[0]
        conn.close()
        return count > 0

    def delete_document_by_path_or_title(self, identifier: str) -> int:
        """Deletes all chunks associated with a specific file path or title."""
        conn = self.get_db_connection()
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM lunaris_documents WHERE file_path = %s OR title = %s",
                (identifier, identifier)
            )
            deleted_count = cur.rowcount
        conn.commit()
        conn.close()
        return deleted_count

    def ingest_file(self, file_path: str, title: Optional[str] = None, force_reindex: bool = False) -> Dict[str, Any]:
        """Processes and indexes a single document into pgvector."""
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_type = path_obj.suffix.lower()
        if file_type not in SUPPORTED_EXTENSIONS:
            return {"status": "skipped", "message": f"Unsupported file type '{file_type}'"}

        file_title = title or path_obj.stem
        file_hash = calculate_file_hash(file_path)

        if not force_reindex and self.is_file_indexed(file_hash):
            return {
                "status": "skipped",
                "title": file_title,
                "message": f"Document '{file_title}' is already up-to-date in vector store."
            }

        # Remove old version if updating existing file
        self.delete_document_by_path_or_title(str(path_obj.resolve()))

        # Extract text & chunk
        content = extract_document_text(file_path)
        chunks = chunk_text(content)

        if not chunks:
            return {"status": "warning", "message": f"No extractable text found in '{file_title}'"}

        conn = self.get_db_connection()
        cur = conn.cursor()

        inserted_count = 0
        for idx, chunk in enumerate(chunks):
            embedding = get_embedding(chunk, model=self.embed_model)
            metadata = {
                "chunk_index": idx,
                "total_chunks": len(chunks),
                "file_size": path_obj.stat().st_size,
                "file_name": path_obj.name,
                "file_type": file_type
            }
            cur.execute(
                """
                INSERT INTO lunaris_documents 
                (title, file_path, file_type, file_hash, chunk_index, chunk_text, metadata, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s::vector)
                """,
                (
                    file_title,
                    str(path_obj.resolve()),
                    file_type,
                    file_hash,
                    idx,
                    chunk,
                    Json(metadata),
                    embedding
                )
            )
            inserted_count += 1

        conn.commit()
        cur.close()
        conn.close()

        return {
            "status": "success",
            "title": file_title,
            "chunks_indexed": inserted_count,
            "file_type": file_type,
            "file_hash": file_hash
        }

    def ingest_directory(self, dir_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """Scans an entire directory and indexes all supported documents."""
        dir_obj = Path(dir_path)
        if not dir_obj.exists() or not dir_obj.is_dir():
            raise NotADirectoryError(f"Directory not found: {dir_path}")

        pattern = "**/*" if recursive else "*"
        results = []
        for file in dir_obj.glob(pattern):
            if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    res_status = str(res.get('status', 'info')).upper()
                    chunks_count = res.get('chunks_indexed', 0)
                    msg = res.get('message', f'Indexed {chunks_count} chunks')
                    print(f"[{res_status}] {file.name}: {msg}")
                except Exception as e:
                    print(f"[ERROR] Failed to ingest {file.name}: {e}")
                    results.append({"status": "error", "file": file.name, "error": str(e)})
        return results

    def list_indexed_documents(self) -> List[Dict[str, Any]]:
        """Returns a summary of all documents currently indexed in pgvector."""
        conn = self.get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT title, file_type, file_path, file_hash, 
                       COUNT(*) as chunk_count, 
                       MIN(created_at) as first_indexed,
                       MAX(created_at) as last_indexed
                FROM lunaris_documents
                GROUP BY title, file_type, file_path, file_hash
                ORDER BY last_indexed DESC;
            """)
            rows = cur.fetchall()
        conn.close()
        return rows

if __name__ == "__main__":
    engine = DocumentIngestionEngine()
    print("=== Lunaris Multi-Format Ingestion Engine ===")
    
    # Ingest default documents directory if exists
    docs_dir = os.path.join(os.path.dirname(__file__), "documents")
    if os.path.exists(docs_dir):
        print(f"Scanning documents directory: {docs_dir}")
        engine.ingest_directory(docs_dir)
    else:
        # Ingest sample file
        sample_path = "sample_knowledge.txt"
        if os.path.exists(sample_path):
            res = engine.ingest_file(sample_path, title="Lunaris Platform Overview")
            print("Sample ingestion result:", res)
