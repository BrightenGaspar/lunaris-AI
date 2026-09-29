# Lunaris Sovereign Architecture Specification

## Overview
Lunaris AI is an autonomous, air-gapped sovereign intelligence platform designed for self-hosting.
It operates without telemetry, external API dependencies, or cloud data leakage.

## Microservices Breakdown
- **Inference Layer**: Ollama local runtime serving quantized GGUF weights.
- **Vector Search**: PostgreSQL 16 + pgvector with HNSW cosine distance indexing.
- **Privacy Search**: SearXNG aggregation metasearch engine.
- **Code Sandbox**: Isolated ephemeral non-networked Docker execution environment.
- **Agent Orchestrator**: ReAct (Reasoning + Acting) loop with scratchpad feedback.

## Security Policies
All sandboxed code runs with memory ceiling of 256MB, CPU quota of 50%, and zero network interface access (`network_mode=none`).
