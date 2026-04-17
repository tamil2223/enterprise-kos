# RAG Playground (UI + API) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a run-based `/playground/*` API and a Next.js UI that visualizes ingestion → chunking (size+overlap) → deterministic fake 384-d embeddings → index mapping → retrieval, including overlap vs no-overlap comparison.

**Architecture:** FastAPI stores per-run artifacts in-memory keyed by `run_id`. Next.js calls the backend and renders artifacts in a stepper UI. Embeddings are behind a replaceable interface (fake now; local/Gemini later).

**Tech Stack:** Python (FastAPI), Next.js (App Router), TypeScript.

---

## File structure (what we’ll add)

### Backend (FastAPI)
- Create: `app/playground/__init__.py`
- Create: `app/playground/models.py`
- Create: `app/playground/store.py`
- Create: `app/playground/chunking.py`
- Create: `app/playground/embeddings.py`
- Create: `app/playground/vector_store.py`
- Create: `app/playground/routes.py`
- Modify: `app/main.py` (include router)

### Tests
- Create: `tests/test_playground_chunking.py`
- Create: `tests/test_playground_vector_store.py`
- Create: `tests/test_playground_api_happy_path.py`

### Frontend (Next.js)
- Create: `web/package.json` (currently missing)
- Create: `web/tsconfig.json`
- Create: `web/tailwind.config.ts`
- Create: `web/postcss.config.mjs`
- Create: `web/next-env.d.ts`
- Create: `web/src/app/layout.tsx`
- Modify: `web/src/app/page.tsx`
- Create: `web/src/lib/api.ts`
- Create: `web/src/lib/types.ts`
- Create: `web/src/components/Stepper.tsx`
- Create: `web/src/components/Artifacts.tsx`

---

### Task 1: Chunking (window + overlap)

**Files:**
- Create: `app/playground/chunking.py`
- Test: `tests/test_playground_chunking.py`

- [ ] **Step 1: Write the failing test**

```python
from app.playground.chunking import chunk_text_window


def test_chunking_overlap_boundaries():
    text = "abcdefghijklmnopqrstuvwxyz" * 10
    chunks = chunk_text_window(text, chunk_size=50, overlap=10, doc_id="d1")
    assert len(chunks) > 1
    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 50
    assert chunks[1].start_char == 40
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_chunking_overlap_boundaries`  
Expected: FAIL (module/function missing).

- [ ] **Step 3: Write minimal implementation**

Implement `chunk_text_window(text, chunk_size, overlap, doc_id)` returning a list of objects containing:
`chunk_id`, `start_char`, `end_char`, `text`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_chunking_overlap_boundaries`  
Expected: PASS.

---

### Task 2: Fake embeddings (384-d deterministic)

**Files:**
- Create: `app/playground/embeddings.py`
- Modify: `tests/test_playground_chunking.py` (add embedding test)

- [ ] **Step 1: Write the failing test**

```python
from app.playground.embeddings import fake_embed_384


def test_fake_embed_dim_and_determinism():
    v1 = fake_embed_384("hello world")
    v2 = fake_embed_384("hello world")
    assert len(v1) == 384
    assert v1 == v2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_fake_embed_dim_and_determinism`  
Expected: FAIL (missing).

- [ ] **Step 3: Write minimal implementation**

Implement signed hashing into 384 buckets + L2 normalization.

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_fake_embed_dim_and_determinism`  
Expected: PASS.

---

### Task 3: Vector store (cosine top-k)

**Files:**
- Create: `app/playground/vector_store.py`
- Test: `tests/test_playground_vector_store.py`

- [ ] **Step 1: Write the failing test**

```python
from app.playground.vector_store import VectorStore


def test_vector_store_topk():
    vs = VectorStore(dim=3)
    vs.add("v1", [1.0, 0.0, 0.0], meta={"chunk_id": "c1"})
    vs.add("v2", [0.0, 1.0, 0.0], meta={"chunk_id": "c2"})
    results = vs.search([1.0, 0.0, 0.0], top_k=1)
    assert results[0].vector_id == "v1"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_vector_store.py::test_vector_store_topk`  
Expected: FAIL (missing).

- [ ] **Step 3: Write minimal implementation**

Implement:
- store normalized vectors
- cosine similarity via dot product
- return sorted results with `vector_id`, `score`, `meta`

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_vector_store.py::test_vector_store_topk`  
Expected: PASS.

---

### Task 4: `/playground/*` API happy path

**Files:**
- Create: `app/playground/models.py`
- Create: `app/playground/store.py`
- Create: `app/playground/routes.py`
- Modify: `app/main.py`
- Test: `tests/test_playground_api_happy_path.py`

- [ ] **Step 1: Write the failing test**

```python
from fastapi.testclient import TestClient


def test_playground_happy_path():
    from app.main import app

    with TestClient(app) as client:
        run = client.post("/playground/runs").json()
        run_id = run["run_id"]

        client.post(f"/playground/runs/{run_id}/documents:load-sample").raise_for_status()
        docs = client.get(f"/playground/runs/{run_id}/documents").json()
        doc_id = docs["documents"][0]["doc_id"]

        client.post(
            f"/playground/runs/{run_id}/chunk",
            json={"doc_id": doc_id, "chunk_size": 500, "overlap": 100},
        ).raise_for_status()
        client.post(f"/playground/runs/{run_id}/embed", json={"doc_id": doc_id}).raise_for_status()
        client.post(f"/playground/runs/{run_id}/index").raise_for_status()

        r = client.post(
            f"/playground/runs/{run_id}/retrieve",
            json={"query": "mcp gateway", "top_k": 5},
        )
        assert r.status_code == 200
        body = r.json()
        assert "results" in body
        assert isinstance(body["results"], list)
        assert len(body["results"]) <= 5
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_api_happy_path.py::test_playground_happy_path`  
Expected: FAIL (routes missing).

- [ ] **Step 3: Write minimal implementation**

Implement endpoints:
- `POST /playground/runs`
- `POST /playground/runs/{run_id}/documents:load-sample`
- `GET /playground/runs/{run_id}/documents`
- `POST /playground/runs/{run_id}/chunk`
- `GET /playground/runs/{run_id}/chunks`
- `POST /playground/runs/{run_id}/embed`
- `POST /playground/runs/{run_id}/index`
- `POST /playground/runs/{run_id}/retrieve`

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_api_happy_path.py::test_playground_happy_path`  
Expected: PASS.

---

### Task 5: Frontend stepper UI (Next.js)

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/tailwind.config.ts`
- Create: `web/postcss.config.mjs`
- Create: `web/next-env.d.ts`
- Create: `web/src/app/layout.tsx`
- Modify: `web/src/app/page.tsx`
- Create: `web/src/lib/api.ts`
- Create: `web/src/lib/types.ts`
- Create: `web/src/components/Stepper.tsx`
- Create: `web/src/components/Artifacts.tsx`

- [ ] **Step 1: Add package.json + install deps**

Run: `cd web && npm install`

- [ ] **Step 2: Implement typed API wrappers**

Add wrappers for each backend endpoint in `web/src/lib/api.ts`.

- [ ] **Step 3: Implement UI**

Single-page stepper that can:
- create run
- load sample docs
- chunking controls + chunk viewer
- embeddings preview matrix
- index mapping preview
- retrieval input + results
- side-by-side comparison: overlap=0 vs overlap=X

- [ ] **Step 4: Run dev server**

Run: `cd web && npm run dev`

---

## Verification

- [ ] Backend: `python3 -m pytest -q`
- [ ] Backend: `uvicorn app.main:app --reload`
- [ ] Frontend: `cd web && npm run dev`
- [ ] End-to-end: complete pipeline in UI on sample docs

# RAG Playground (UI + API) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a run-based `/playground/*` API and a Next.js UI that visualizes ingestion → chunking (size+overlap) → fake 384-d embeddings → index mapping → retrieval, including overlap vs no-overlap comparison.

**Architecture:** FastAPI stores per-run artifacts in memory keyed by `run_id`. Next.js calls the backend and renders artifacts in a stepper UI. Embeddings are deterministic fake vectors behind a replaceable interface.

**Tech Stack:** Python (FastAPI), Next.js (App Router), TypeScript, fetch JSON APIs.

---

## File structure (what we’ll add)

### Backend (FastAPI)
- Create: `app/playground/__init__.py`
- Create: `app/playground/models.py` (RunState + Pydantic schemas)
- Create: `app/playground/store.py` (in-memory store keyed by run_id)
- Create: `app/playground/chunking.py` (window + overlap chunker)
- Create: `app/playground/embeddings.py` (fake 384-d embedding + interface)
- Create: `app/playground/vector_store.py` (in-memory vector index + cosine search)
- Create: `app/playground/routes.py` (APIRouter for `/playground/*`)
- Modify: `app/main.py` (include router)

### Tests
- Create: `tests/test_playground_chunking.py`
- Create: `tests/test_playground_api_happy_path.py`

### Frontend (Next.js)
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/postcss.config.mjs`
- Create: `web/tailwind.config.ts`
- Create: `web/next-env.d.ts`
- Create: `web/src/app/layout.tsx`
- Modify: `web/src/app/page.tsx` (RAG Playground UI)
- Create: `web/src/lib/api.ts` (typed client wrappers)
- Create: `web/src/lib/types.ts` (frontend types)
- Create: `web/src/components/Stepper.tsx`
- Create: `web/src/components/Artifacts.tsx` (chunks/embeddings/index/retrieval)

---

## Task 1: Backend chunking module (window + overlap)

**Files:**
- Create: `app/playground/chunking.py`
- Test: `tests/test_playground_chunking.py`

- [ ] **Step 1: Write failing test for overlap boundaries**

```python
from app.playground.chunking import chunk_text_window


def test_chunking_overlap_boundaries():
    text = "abcdefghijklmnopqrstuvwxyz" * 10
    chunks = chunk_text_window(text, chunk_size=50, overlap=10, doc_id="d1")
    assert len(chunks) > 1
    assert chunks[0].start_char == 0
    assert chunks[0].end_char == 50
    assert chunks[1].start_char == 40  # 50 - 10
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_chunking_overlap_boundaries`  
Expected: FAIL (module/function missing).

- [ ] **Step 3: Implement `chunk_text_window`**

Implement in `app/playground/chunking.py`:
- validate `overlap < chunk_size`
- sliding window chunks with deterministic ids `f"{doc_id}#chunk-{i}"`
- include offsets + text

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_chunking_overlap_boundaries`  
Expected: PASS.

---

## Task 2: Fake embeddings (384-d deterministic)

**Files:**
- Create: `app/playground/embeddings.py`
- Modify: `tests/test_playground_chunking.py` (add deterministic embed test) OR create `tests/test_playground_embeddings.py`

- [ ] **Step 1: Write failing test for determinism + dim**

```python
from app.playground.embeddings import fake_embed_384


def test_fake_embed_dim_and_determinism():
    v1 = fake_embed_384("hello world")
    v2 = fake_embed_384("hello world")
    assert len(v1) == 384
    assert v1 == v2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_fake_embed_dim_and_determinism`  
Expected: FAIL (missing).

- [ ] **Step 3: Implement `fake_embed_384`**

Implementation details:
- tokenize words
- signed hashing into 384 buckets
- L2 normalize vector

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_chunking.py::test_fake_embed_dim_and_determinism`  
Expected: PASS.

---

## Task 3: Vector store (cosine top-k)

**Files:**
- Create: `app/playground/vector_store.py`
- Create: `tests/test_playground_vector_store.py`

- [ ] **Step 1: Write failing test for top-k retrieval**

```python
from app.playground.vector_store import VectorStore


def test_vector_store_topk():
    vs = VectorStore(dim=3)
    vs.add("v1", [1.0, 0.0, 0.0], meta={"chunk_id": "c1"})
    vs.add("v2", [0.0, 1.0, 0.0], meta={"chunk_id": "c2"})
    results = vs.search([1.0, 0.0, 0.0], top_k=1)
    assert results[0].vector_id == "v1"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest -q tests/test_playground_vector_store.py::test_vector_store_topk`  
Expected: FAIL (missing).

- [ ] **Step 3: Implement minimal vector store**

Implement:
- store normalized vectors
- cosine similarity via dot product
- return sorted results with `vector_id`, `score`, `meta`

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest -q tests/test_playground_vector_store.py::test_vector_store_topk`  
Expected: PASS.

---

## Task 4: Run store + API routes (happy path)

**Files:**
- Create: `app/playground/store.py`
- Create: `app/playground/models.py`
- Create: `app/playground/routes.py`
- Modify: `app/main.py`
- Create: `tests/test_playground_api_happy_path.py`

- [ ] **Step 1: Write failing API test for happy path**

```python
from fastapi.testclient import TestClient


def test_playground_happy_path():
    from app.main import app

    with TestClient(app) as client:
        run = client.post("/playground/runs").json()
        run_id = run["run_id"]

        client.post(f"/playground/runs/{run_id}/documents:load-sample").raise_for_status()
        docs = client.get(f"/playground/runs/{run_id}/documents").json()
        doc_id = docs["documents"][0]["doc_id"]

        client.post(f"/playground/runs/{run_id}/chunk", json={\"doc_id\": doc_id, \"chunk_size\": 500, \"overlap\": 100}).raise_for_status()
        client.post(f\"/playground/runs/{run_id}/embed\", json={\"doc_id\": doc_id}).raise_for_status()
        client.post(f\"/playground/runs/{run_id}/index\").raise_for_status()

        r = client.post(f\"/playground/runs/{run_id}/retrieve\", json={\"query\": \"mcp gateway\", \"top_k\": 5})\n        assert r.status_code == 200\n+        body = r.json()\n+        assert \"results\" in body\n+        assert isinstance(body[\"results\"], list)\n+        assert len(body[\"results\"]) <= 5\n+```\n+\n+- [ ] **Step 2: Run test to verify it fails**\n+\n+Run: `python3 -m pytest -q tests/test_playground_api_happy_path.py::test_playground_happy_path`  \n+Expected: FAIL (routes missing).\n+\n+- [ ] **Step 3: Implement minimal `/playground/*` routes**\n+\n+Key implementation constraints:\n+- Run store is in-memory dict\n+- Sample docs are built-in strings (2–5)\n+- Chunking uses `chunk_text_window`\n+- Embedding uses `fake_embed_384`\n+- Index builds VectorStore with mapping chunk_id ↔ vector_id\n+\n+- [ ] **Step 4: Run test to verify it passes**\n+\n+Run: `python3 -m pytest -q tests/test_playground_api_happy_path.py::test_playground_happy_path`  \n+Expected: PASS.\n+\n+---\n+\n+## Task 5: Frontend scaffolding (Next.js) + stepper UI\n+\n+**Files:**\n+- Create: `web/package.json`\n+- Create: `web/tsconfig.json`\n+- Create: `web/tailwind.config.ts`\n+- Create: `web/postcss.config.mjs`\n+- Create: `web/next-env.d.ts`\n+- Create: `web/src/app/layout.tsx`\n+- Modify: `web/src/app/page.tsx`\n+- Create: `web/src/lib/api.ts`\n+- Create: `web/src/lib/types.ts`\n+- Create: `web/src/components/Stepper.tsx`\n+- Create: `web/src/components/Artifacts.tsx`\n+\n+- [ ] **Step 1: Add a minimal `package.json` with Next + React + Tailwind**\n+\n+- [ ] **Step 2: Implement `api.ts` wrappers**\n+\n+Functions:\n+- `createRun()`\n+- `loadSample(runId)`\n+- `listDocs(runId)`\n+- `chunk(runId, docId, chunkSize, overlap)`\n+- `embed(runId, docId)`\n+- `index(runId)`\n+- `retrieve(runId, query, topK)`\n+\n+- [ ] **Step 3: Build `page.tsx` stepper UI**\n+\n+UI requirements:\n+- create or reuse a `run_id` in state\n+- Ingestion step: “Load sample data” button + doc list\n+- Chunking step: chunk size + overlap inputs + chunk list viewer\n+- Retrieval compare: toggle overlap=0 vs overlap=X and show results side-by-side\n+\n+- [ ] **Step 4: Run frontend dev server**\n+\n+Run (example): `cd web && npm install && npm run dev`\n+\n+---\n+\n+## Verification\n+\n+- [ ] Run backend tests: `python3 -m pytest -q`\n+- [ ] Run backend server: `uvicorn app.main:app --reload`\n+- [ ] Open UI and complete pipeline on sample docs\n+\n*** End Patch"}]} скорее fails? It's huge; patch broken due to stray plus markers. need reapply properly. We'll not include within patch with stray markers. We'll rewrite plan file from scratch carefully. Let's delete and add simpler plan without code blocks that include '+'.
