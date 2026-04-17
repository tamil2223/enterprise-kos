## Enterprise Knowledge OS (KOS) — v1 Design Spec

### Goal
Deliver a functional, demonstrable **v1 MVP backend** that proves:
- A clean **API façade** for an “AI knowledge OS”
- A **context gateway** boundary (MCP-like layer) that standardizes/filters context before LLM calls
- A minimal **agentic workflow** boundary (router → researcher → synthesizer)

v1 optimizes for: clarity of architecture, runnable demo, extensibility.  
v1 does **not** optimize for: enterprise scaling, RBAC, Kafka streaming, production observability.

### Non-goals (explicitly deferred to v2/v3)
- Streaming ingestion (Kafka)
- RBAC / tenant isolation
- Deep observability (LangSmith/Prometheus), tracing, analytics dashboards
- Redis-backed memory/caching
- Cross-encoder reranking
- Frontend dashboard / chrome extension integration (beyond a stable REST API)

### Repository & layout
Create a new project folder:
`/Users/tamil-work/Documents/Work/personal/ai-engg/enterprise-kos/`

Proposed layout (v1):
```
enterprise-kos/
  README.md
  requirements.txt
  .env.example
  .gitignore
  app/
    __init__.py
    main.py
    api/
      __init__.py
      routes.py
    core/
      __init__.py
      config.py
    mcp/
      __init__.py
      gateway.py
      schemas.py
    agents/
      __init__.py
      router.py
      researcher.py
      synthesizer.py
      runner.py
    rag/
      __init__.py
      retrieve.py
      ingest.py
```

Notes:
- Keep modules small and interface-driven: `rag/*` provides retrieval primitives, `mcp/*` defines context contracts, `agents/*` composes steps, `api/*` exposes HTTP.
- v1 can stub out ingestion/retrieval with an in-memory index or simple local files; PGVector/BM25 integration can be introduced behind `rag/retrieve.py` without changing API contracts.

### API surface (v1)
FastAPI server exposing:

- `POST /query`
  - Purpose: single-shot Q&A using the MCP context gateway + synthesizer.
  - Request (draft):
    - `query: str`
    - `top_k: int = 5`
    - `filters: dict | null` (future-proofing)
  - Response (draft):
    - `answer: str`
    - `contexts: [ContextItem]` (the context injected into the LLM)
    - `sources: [Source]` (optional; derived from contexts)

- `GET /context`
  - Purpose: inspect what context would be selected for a query (debugging + transparency).
  - Params: `q: str`, `top_k: int = 5`
  - Response: `contexts: [ContextItem]`

- `POST /agent/run`
  - Purpose: run the multi-step agent pipeline and return intermediate artifacts.
  - Request:
    - `query: str`
    - `mode: "default" | "research" | ...` (optional)
  - Response:
    - `final: str`
    - `steps: [{name, input, output}]`
    - `contexts: [ContextItem]`

All endpoints return JSON and have OpenAPI docs at `/docs`.

### MCP-like Context Gateway (v1)
Goal: enforce a boundary between retrieval and generation.

Responsibilities:
- Accept a query (and optional filters) and return a **standardized context bundle**:
  - Each context item includes: `id`, `title`, `text`, `source`, `score`, `metadata`
- Apply basic policy hooks (v1):
  - Max total characters / tokens (simple char-based limit in v1)
  - Dedup similar snippets (heuristic)
- Format contexts for the LLM (v1):
  - Provide a structured JSON-like object to the LLM prompt
  - Include explicit provenance fields

Non-goals (v1):
- Auth/RBAC enforcement
- Tenant-scoped data policies

### RAG layer (v1)
Goal: retrieval primitives behind a stable interface.

v1 retrieval strategy options:
- **Option A (minimal, fastest)**: local file corpus (e.g., `data/`) + simple keyword scoring
- **Option B (still light)**: local embeddings + FAISS for semantic search
- **Option C (closest to README)**: Postgres + PGVector + BM25 hybrid

Recommendation for v1: start with **Option A** (or B) to keep the MVP runnable without external services; design the `rag/retrieve.py` interface so swapping in PGVector/BM25 later is straightforward.

### Agentic orchestration (v1)
Goal: show a clear multi-step workflow with clean boundaries.

Pipeline:
- **Router**: classify query into a small set of routes (e.g., “direct_answer” vs “needs_retrieval”).
- **Researcher**: call MCP gateway to fetch contexts; optionally perform lightweight “search” (stubbed).
- **Synthesizer**: produce final answer from query + contexts with explicit citations/provenance.

Implementation note:
- If LangGraph is already a dependency preference, encapsulate it in `agents/runner.py`. Otherwise implement the same pipeline in plain Python first; add LangGraph later without changing API.

### Configuration (v1)
`.env.example` includes:
- `APP_ENV=dev`
- `HOST=0.0.0.0`
- `PORT=8000`
- `CONTEXT_MAX_CHARS=8000`
- `TOP_K_DEFAULT=5`
- `LLM_PROVIDER=...` (optional in v1; can be stubbed)

### Testing (v1)
- Minimal smoke tests:
  - app imports
  - `/docs` loads
  - `/context` returns an array
  - `/agent/run` returns `final` and `steps`

### Success criteria (v1)
- `uvicorn app.main:app --reload` runs locally from a fresh clone.
- `POST /agent/run` returns a deterministic structured response shape.
- The context gateway returns standardized, bounded contexts with provenance fields.
- Repo README matches the runnable code (no broken commands/paths).

