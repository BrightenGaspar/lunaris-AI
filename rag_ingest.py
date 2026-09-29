import os
import sys
import requests
import psycopg2
from psycopg2.extras import Json

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lunaris_ai"),
    "user": os.getenv("DB_USER", "lunaris"),
    "password": os.getenv("DB_PASSWORD", "lunaris_secure_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

def get_embedding(text: str, model: str = "nomic-embed-text") -> list[float]:
    res = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": model, "prompt": text})
    res.raise_for_status()
    return res.json().get("embedding", [])

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    step = max(1, chunk_size - overlap)
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def ingest_file(file_path: str, title: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    chunks = chunk_text(content)
    if not chunks:
        print(f"No content to ingest in '{file_path}'")
        return

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    for idx, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        metadata = {"chunk_index": idx, "source": file_path, "total_chunks": len(chunks)}
        cur.execute(
            """
            INSERT INTO lunaris_documents (title, chunk_text, metadata, embedding)
            VALUES (%s, %s, %s, %s::vector)
            """,
            (title, chunk, Json(metadata), embedding)
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"Successfully ingested {len(chunks)} chunks from '{title}'.")

if __name__ == "__main__":
    sample_path = "sample_knowledge.txt"
    if not os.path.exists(sample_path):
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write(
                "Lunaris AI is a sovereign, self-hosted artificial intelligence platform designed for complete data privacy.\n"
                "It integrates local LLM inference via Ollama, pgvector semantic search, private metasearch via SearXNG,\n"
                "and an isolated Docker sandbox for safe code execution."
            )
    ingest_file(sample_path, title="Lunaris Architecture Overview")
