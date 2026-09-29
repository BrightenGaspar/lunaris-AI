-- Enable pgvector and uuid extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Document chunks table for Lunaris RAG
CREATE TABLE IF NOT EXISTS lunaris_documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding vector(768), -- Dimensions for nomic-embed-text / bge-base-en-v1.5
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Fast HNSW Index for Cosine Distance
CREATE INDEX IF NOT EXISTS lunaris_doc_hnsw_idx 
ON lunaris_documents USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);

-- Conversational Sessions & Memory
CREATE TABLE IF NOT EXISTS lunaris_conversations (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('system', 'user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    tool_calls JSONB DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_lunaris_session_id ON lunaris_conversations(session_id);
