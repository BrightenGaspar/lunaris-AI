import os
import json
import math
import requests
from typing import Dict, Any, List
from sandbox import CodeExecutionSandbox

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080/search")
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lunaris_ai"),
    "user": os.getenv("DB_USER", "lunaris"),
    "password": os.getenv("DB_PASSWORD", "lunaris_secure_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

sandbox_instance = CodeExecutionSandbox()

class LunarisToolRegistry:
    """Registry of sovereign tools executable by the ReAct agent."""

    @staticmethod
    def get_embedding(text: str) -> list[float]:
        try:
            res = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": text}, timeout=15)
            res.raise_for_status()
            return res.json().get("embedding", [])
        except Exception:
            return [0.0] * 768

    @classmethod
    def search_documents(cls, query: str, top_k: int = 4) -> str:
        """Searches indexed documents in pgvector using semantic cosine similarity."""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            query_vector = cls.get_embedding(query)
            conn = psycopg2.connect(**DB_CONFIG)
            sql = """
                SELECT title, chunk_text, (embedding <=> %s::vector) AS distance, metadata
                FROM lunaris_documents
                ORDER BY distance ASC
                LIMIT %s;
            """
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, (query_vector, top_k))
                rows = cur.fetchall()
            conn.close()

            if not rows:
                return "No relevant documents found in the local knowledge base."

            formatted = []
            for i, r in enumerate(rows):
                sim = round(1.0 - float(r["distance"]), 3)
                formatted.append(f"[{i+1}] Source: '{r['title']}' (Similarity: {sim})\n{r['chunk_text']}")
            return "\n\n---\n\n".join(formatted)
        except Exception as e:
            return f"Document vector database offline or connecting: {e}"

    @staticmethod
    def web_search(query: str, limit: int = 4) -> str:
        """Performs a live private internet metasearch via local SearXNG."""
        try:
            params = {"q": query, "format": "json"}
            res = requests.get(SEARXNG_URL, params=params, timeout=8)
            results = res.json().get("results", [])
            if not results:
                return f"No search results returned for query: '{query}'."

            formatted = []
            for r in results[:limit]:
                title = r.get("title", "No Title")
                snippet = r.get("content", "")
                url = r.get("url", "")
                formatted.append(f"• Title: {title}\n  URL: {url}\n  Snippet: {snippet}")
            return "\n\n".join(formatted)
        except Exception as e:
            return f"SearXNG metasearch offline or connecting: {e}"

    @staticmethod
    def execute_python_sandbox(code: str) -> str:
        """Executes untrusted Python code inside an isolated sandbox."""
        res = sandbox_instance.execute_python(code)
        if res["status"] == "success":
            return f"[Execution Output]:\n{res['output']}"
        elif res["status"] == "runtime_error":
            return f"[Runtime Error]:\n{res['output']}"
        else:
            return f"[Execution Failed]: {res['output']}"

    @staticmethod
    def calculate_math(expression: str) -> str:
        """Safely evaluates mathematical expressions."""
        try:
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "min": min, "max": max, "sum": sum, "pow": pow})
            code = compile(expression, "<string>", "eval")
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of '{name}' is not permitted.")
            result = eval(code, {"__builtins__": {}}, allowed_names)
            return f"Result: {result}"
        except Exception as e:
            return f"Calculation error: {e}"

    @staticmethod
    def list_knowledge_base() -> str:
        """Lists all documents currently indexed in the local vector database."""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT title, file_type, COUNT(*) as chunks, MAX(created_at) as indexed_at
                    FROM lunaris_documents
                    GROUP BY title, file_type
                    ORDER BY indexed_at DESC;
                """)
                rows = cur.fetchall()
            conn.close()
            if not rows:
                return "The local knowledge base is currently empty."
            items = [f"• {r['title']} ({r['file_type']}) - {r['chunks']} chunks" for r in rows]
            return "Indexed Documents in Lunaris AI:\n" + "\n".join(items)
        except Exception as e:
            return f"Database query note: {e}"

    @staticmethod
    def generate_image(prompt: str) -> str:
        """Generates an image via local Stable Diffusion / ComfyUI."""
        sd_url = "http://localhost:7860/sdapi/v1/txt2img"
        payload = {"prompt": prompt, "steps": 25, "width": 1024, "height": 1024}
        try:
            res = requests.post(sd_url, json=payload, timeout=60)
            res.raise_for_status()
            import base64
            img_b64 = res.json()["images"][0]
            output_file = f"gen_output.png"
            with open(output_file, "wb") as f:
                f.write(base64.b64decode(img_b64))
            return f"Image successfully saved to {output_file}"
        except Exception as e:
            return f"Image generation unavailable: {e}"

TOOL_DEFINITIONS = [
    {
        "name": "search_documents",
        "description": "Searches local internal documents and knowledge base using semantic vector search.",
        "parameters": {"query": "string"}
    },
    {
        "name": "web_search",
        "description": "Searches the live public internet using private SearXNG.",
        "parameters": {"query": "string"}
    },
    {
        "name": "execute_python_sandbox",
        "description": "Executes Python code in a secure sandbox.",
        "parameters": {"code": "string"}
    },
    {
        "name": "calculate_math",
        "description": "Evaluates pure mathematical expressions (e.g. 'sqrt(144) * 3.14159', '2**16').",
        "parameters": {"expression": "string"}
    },
    {
        "name": "list_knowledge_base",
        "description": "Returns a list of all documents currently indexed in the Lunaris knowledge base.",
        "parameters": {}
    }
]
