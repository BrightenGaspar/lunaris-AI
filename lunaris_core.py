import os
import uuid
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from sandbox import CodeExecutionSandbox

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080/search")
COMFYUI_URL = os.getenv("COMFYUI_URL", "http://localhost:8188")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lunaris_ai"),
    "user": os.getenv("DB_USER", "lunaris"),
    "password": os.getenv("DB_PASSWORD", "lunaris_secure_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

class LunarisEngine:
    def __init__(self, llm_model: str = "llama3.3", embed_model: str = "nomic-embed-text"):
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.sandbox = CodeExecutionSandbox()

    # 1. Text Generation
    def generate_response(self, prompt: str, system_prompt: str = "") -> str:
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
        }
        res = requests.post(f"{OLLAMA_URL}/api/generate", json=payload)
        res.raise_for_status()
        return res.json().get("response", "")

    # 2. Local Embeddings (Ollama)
    def embed_text(self, text: str) -> list[float]:
        payload = {"model": self.embed_model, "prompt": text}
        res = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload)
        res.raise_for_status()
        return res.json().get("embedding", [])

    # 3. Document Vector Search (pgvector)
    def query_knowledge_base(self, query: str, top_k: int = 3) -> list[str]:
        query_vector = self.embed_text(query)
        sql = """
            SELECT chunk_text, (embedding <=> %s::vector) AS distance
            FROM lunaris_documents
            ORDER BY distance ASC
            LIMIT %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (query_vector, top_k))
            rows = cur.fetchall()
        return [r["chunk_text"] for r in rows]

    # 4. Local Metasearch (SearXNG)
    def web_search(self, query: str, limit: int = 3) -> list[str]:
        params = {"q": query, "format": "json"}
        try:
            res = requests.get(SEARXNG_URL, params=params, timeout=5)
            results = res.json().get("results", [])
            return [f"[{r.get('title')}]: {r.get('content')}" for r in results[:limit]]
        except Exception:
            return []

    # 5. Local Image Generation (ComfyUI / SD API standard)
    def generate_image(self, prompt: str, output_path: str = "output.png") -> str:
        sd_url = "http://localhost:7860/sdapi/v1/txt2img"
        payload = {
            "prompt": prompt,
            "steps": 25,
            "width": 1024,
            "height": 1024
        }
        try:
            res = requests.post(sd_url, json=payload, timeout=60)
            res.raise_for_status()
            import base64
            img_b64 = res.json()["images"][0]
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(img_b64))
            return f"Image saved to {output_path}"
        except Exception as e:
            return f"Image Generation Failed: {e}"

    # 6. Isolated Code Execution
    def execute_code(self, code: str) -> dict:
        return self.sandbox.execute_python(code)

    # 7. Autonomous Context Router & Conversation Memory
    def run_agent(self, user_query: str, session_id: str | None = None, use_web: bool = False, use_docs: bool = False) -> str:
        contexts = []
        if use_docs:
            doc_context = self.query_knowledge_base(user_query)
            if doc_context:
                contexts.append("Local Document Context:\n" + "\n---\n".join(doc_context))

        if use_web:
            web_context = self.web_search(user_query)
            if web_context:
                contexts.append("Live Web Search Context:\n" + "\n---\n".join(web_context))

        context_str = "\n\n".join(contexts)
        prompt = (
            f"Context Information:\n{context_str}\n\nUser Question: {user_query}"
            if contexts else user_query
        )
        system = "You are Lunaris AI, a private self-hosted sovereign intelligence system. Answer directly and concisely."

        response = self.generate_response(prompt=prompt, system_prompt=system)

        if session_id:
            try:
                valid_uuid = uuid.UUID(session_id)
                with self.conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO lunaris_conversations (session_id, role, content) VALUES (%s, %s, %s)",
                        (str(valid_uuid), "user", user_query)
                    )
                    cur.execute(
                        "INSERT INTO lunaris_conversations (session_id, role, content) VALUES (%s, %s, %s)",
                        (str(valid_uuid), "assistant", response)
                    )
                    self.conn.commit()
            except Exception as e:
                print(f"Memory logging warning: {e}")

        return response

if __name__ == "__main__":
    agent = LunarisEngine(llm_model="llama3.3")
    print("Lunaris AI Core Initialized.")
