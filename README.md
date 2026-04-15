# 🧠 Enterprise Knowledge OS (KOS)

An AI platform featuring a custom Model Context Protocol (MCP) gateway, Hybrid RAG, and Multi-Agent Orchestration.

![Python](https://img.shields.io/badge/Python-FastAPI-blue)
![AI](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)
![DB](https://img.shields.io/badge/PGVector-Hybrid_RAG-green)
![Status](https://img.shields.io/badge/Status-v1_Active_Development-brightgreen)

## 📖 Overview

Enterprise AI fails when Large Language Models (LLMs) lack secure, standardized, and relevant context.

**Enterprise KOS** is a production-grade backend system designed to solve the “last mile” of AI integration:
it ingests enterprise data (Docs, APIs, DBs), standardizes it through a custom **MCP Context Gateway**, and orchestrates complex decision workflows using a **multi-agent system**.

Instead of treating LLMs as standalone chatbots, KOS acts as an **API gateway for AI**.

## 🏗️ High-Level Architecture

```
[Data Sources] (PDFs, DBs, APIs)
       ⬇
[Ingestion & Chunking Pipeline]
       ⬇
[Hybrid Retrieval Layer] (Semantic + BM25 + optional re-rank)
       ⬇
[⚙️ MCP Context Gateway]  (standardizes, filters, formats context)
       ⬇
[🧠 Multi-Agent Orchestration] (Router → Researcher → Synthesizer)
       ⬇
[FastAPI Interface]  (REST API for UIs, extensions, enterprise tools)
```

## ✨ Core Features

- **Model Context Protocol (MCP) Gateway**: A secure abstraction layer that fetches relevant knowledge, manages context scope, and formats it cleanly before it ever reaches the LLM.
- **Hybrid RAG**: Combines semantic retrieval with keyword matching (BM25) and an extensible reranking slot to reduce hallucinations.
- **Agentic Orchestration**: Multi-step reasoning. Agents plan, retrieve via MCP, and synthesize answers with provenance.
- **Enterprise-ready backend**: Built on FastAPI with async-friendly boundaries, designed for low-latency inference and scale-up.

## 🚀 Roadmap & Phased Delivery

### Phase v1: Core Engine & MVP (Current)

The foundational architecture proving the MCP boundary and the agentic workflow.

- [x] **API layer**: FastAPI setup with `POST /query`, `GET /context`, and `POST /agent/run`
- [x] **Ingestion**: Basic document (PDF/TXT) and API ingestion pipeline (MVP scope)
- [x] **RAG layer**: Hybrid retrieval boundary (semantic + keyword), behind a stable interface
- [x] **MCP layer**: Standardized JSON context injection for LLMs
- [x] **Multi-agent system**: Router, Researcher, Synthesizer workflow

### Phase v2: Scale, Observability & Resilience (Next)

Upgrading the system to handle high-volume enterprise workloads.

- [ ] **Streaming ingestion**: Kafka integration for real-time ingestion
- [ ] **Advanced memory**: Redis-backed short-term memory + context caching
- [ ] **Security & RBAC**: Permission-aware retrieval in MCP (who can see what)
- [ ] **Observability**: LangSmith and/or Prometheus metrics (tokens, latency, step traces)
- [ ] **Advanced RAG**: Cross-encoder reranking for high-precision retrieval

### Phase v3: Interfaces & Optimization (Future)

The UX layer and cost-management features.

- [ ] **Cost-aware LLM routing**: Route subtasks to cheaper/faster models; reserve premium models for synthesis
- [ ] **Frontend application**: Next.js dashboard for tracing, runs, and knowledge management
- [ ] **Edge integration**: Chrome extension to interact with KOS securely from any browser tab

## 🛠️ Tech Stack

- **Core API**: Python 3.11+, FastAPI, Uvicorn
- **AI & orchestration**: LangChain, LangGraph, OpenAI/Gemini APIs
- **Database & retrieval**: PostgreSQL (PGVector), FAISS, Redis
- **DevOps (v2)**: Docker, Docker Compose, GitHub Actions (CI/CD)

## ⚡ Quick Start (v1)

```bash
# Clone the repository
git clone https://github.com/tamil2223/enterprise-kos.git
cd enterprise-kos

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env

# Run the FastAPI server
uvicorn app.main:app --reload
```

Swagger UI will be available at `http://localhost:8000/docs`.

## Why this README is intentionally phased

- **It proves architectural thinking**: clear boundaries (Ingestion vs Retrieval vs MCP vs Agents vs API).
- **It avoids scope creep**: v1 proves the core context injection + orchestration; v2 adds scale/security/observability; v3 adds UX and cost controls.
- **It’s interview-friendly**: you can explain trade-offs without pretending v1 already solves enterprise scale.

