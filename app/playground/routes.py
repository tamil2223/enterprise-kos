from __future__ import annotations

import hashlib
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.playground.chunking import chunk_text_window
from app.playground.embeddings import fake_embed_384
from app.playground.models import (
    ChunkRequest,
    ChunkResponse,
    CreateRunResponse,
    Document,
    ListDocumentsResponse,
    RunSummaryResponse,
    RetrieveRequest,
    RetrieveResponse,
    RetrieveResult,
    EmbedRequest,
    EmbedResponse,
    IndexResponse,
    IndexState,
    EmbeddingState,
    DocumentInfo,
    ChunkInfo,
    preview_text,
    preview_vector,
)
from app.playground.store import store
from app.playground.vector_store import VectorStore


router = APIRouter(prefix="/playground", tags=["playground"])


def _get_run_or_404(run_id: str):
    try:
        return store.get_run(run_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="run not found")


@router.post("/runs", response_model=CreateRunResponse)
def create_run() -> CreateRunResponse:
    run = store.create_run()
    return CreateRunResponse(run_id=run.run_id)


@router.get("/runs/{run_id}", response_model=RunSummaryResponse)
def get_run_summary(run_id: str) -> RunSummaryResponse:
    run = _get_run_or_404(run_id)
    indexed = 0 if run.index is None else len(run.index.chunk_id_by_vector_id)
    return RunSummaryResponse(
        run_id=run.run_id,
        documents_count=len(run.documents),
        chunked_docs_count=len(run.chunks),
        embedded_docs_count=len(run.embeddings),
        indexed_vectors_count=indexed,
        has_documents=len(run.documents) > 0,
        has_chunks=len(run.chunks) > 0,
        has_embeddings=len(run.embeddings) > 0,
        has_index=run.index is not None,
    )


@router.post("/runs/{run_id}/documents:load-sample")
def load_sample_documents(run_id: str) -> dict:
    run = _get_run_or_404(run_id)
    samples = [
        (
            "mcp_gateway.md",
            "text/markdown",
            "MCP context gateway\n\nResponsibilities: selection, normalization, budgeting, provenance, and policy hooks (RBAC, redaction).",
        ),
        (
            "hybrid_rag.txt",
            "text/plain",
            "Hybrid retrieval combines semantic (dense) and lexical (BM25) signals. Reranking can improve precision.",
        ),
        (
            "observability.txt",
            "text/plain",
            "Observability: step traces, retrieval metrics, token/latency metrics per agent step and per endpoint.",
        ),
    ]

    run.documents.clear()
    run.chunks.clear()
    run.chunk_params.clear()
    run.embeddings.clear()
    run.index = None
    for name, ct, text in samples:
        doc_id = hashlib.sha1(f"{run_id}:{name}".encode("utf-8")).hexdigest()[:12]
        run.documents[doc_id] = Document(doc_id=doc_id, name=name, content_type=ct, text=text)
    return {"loaded": len(run.documents)}


@router.post("/runs/{run_id}/documents:upload")
async def upload_documents(run_id: str, files: list[UploadFile] = File(...)) -> dict:
    run = _get_run_or_404(run_id)
    loaded = 0
    for f in files:
        filename = f.filename or "upload.txt"
        suffix = Path(filename).suffix.lower()
        if suffix not in {".txt", ".md"}:
            raise HTTPException(status_code=400, detail="only .txt and .md uploads are supported in v1")
        raw = await f.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("utf-8", errors="replace")

        ct = "text/markdown" if suffix == ".md" else "text/plain"
        doc_id = hashlib.sha1(f"{run_id}:{filename}:{len(text)}".encode("utf-8")).hexdigest()[:12]
        run.documents[doc_id] = Document(doc_id=doc_id, name=filename, content_type=ct, text=text)
        loaded += 1

    return {"uploaded": loaded}


@router.get("/runs/{run_id}/documents", response_model=ListDocumentsResponse)
def list_documents(run_id: str) -> ListDocumentsResponse:
    run = _get_run_or_404(run_id)
    docs = [
        DocumentInfo(
            doc_id=d.doc_id,
            name=d.name,
            content_type=d.content_type,
            size_chars=len(d.text),
        )
        for d in run.documents.values()
    ]
    return ListDocumentsResponse(documents=docs)


@router.post("/runs/{run_id}/chunk", response_model=ChunkResponse)
def run_chunking(run_id: str, req: ChunkRequest) -> ChunkResponse:
    run = _get_run_or_404(run_id)
    if req.doc_id not in run.documents:
        raise HTTPException(status_code=404, detail="doc not found")

    doc = run.documents[req.doc_id]
    chunks = chunk_text_window(text=doc.text, chunk_size=req.chunk_size, overlap=req.overlap, doc_id=req.doc_id)
    run.chunks[req.doc_id] = chunks
    run.chunk_params[req.doc_id] = (req.chunk_size, req.overlap)

    infos = [
        ChunkInfo(
            chunk_id=c.chunk_id,
            doc_id=c.doc_id,
            chunk_index=c.chunk_index,
            start_char=c.start_char,
            end_char=c.end_char,
            text_preview=preview_text(c.text),
        )
        for c in chunks
    ]
    return ChunkResponse(doc_id=req.doc_id, chunk_size=req.chunk_size, overlap=req.overlap, chunks=infos)


@router.get("/runs/{run_id}/chunks", response_model=ChunkResponse)
def list_chunks(run_id: str, doc_id: str) -> ChunkResponse:
    run = _get_run_or_404(run_id)
    chunks = run.chunks.get(doc_id, [])
    chunk_size, overlap = run.chunk_params.get(doc_id, (0, 0))
    infos = [
        ChunkInfo(
            chunk_id=c.chunk_id,
            doc_id=c.doc_id,
            chunk_index=c.chunk_index,
            start_char=c.start_char,
            end_char=c.end_char,
            text_preview=preview_text(c.text),
        )
        for c in chunks
    ]
    return ChunkResponse(doc_id=doc_id, chunk_size=chunk_size, overlap=overlap, chunks=infos)


@router.post("/runs/{run_id}/embed", response_model=EmbedResponse)
def embed_chunks(run_id: str, req: EmbedRequest) -> EmbedResponse:
    run = _get_run_or_404(run_id)
    chunks = run.chunks.get(req.doc_id)
    if not chunks:
        raise HTTPException(status_code=400, detail="no chunks for doc_id; run chunking first")

    state = EmbeddingState(dim=384)
    for c in chunks:
        vec = fake_embed_384(c.text)
        vid = hashlib.sha1(c.chunk_id.encode("utf-8")).hexdigest()[:16]
        state.vector_by_chunk_id[c.chunk_id] = vec
        state.vector_id_by_chunk_id[c.chunk_id] = vid

    run.embeddings[req.doc_id] = state

    mapping_preview = [
        {"chunk_id": cid, "vector_id": vid}
        for cid, vid in list(state.vector_id_by_chunk_id.items())[:20]
    ]
    vectors_preview = [preview_vector(v) for v in list(state.vector_by_chunk_id.values())[:10]]
    return EmbedResponse(doc_id=req.doc_id, dim=state.dim, mapping_preview=mapping_preview, vectors_preview=vectors_preview)


@router.post("/runs/{run_id}/index", response_model=IndexResponse)
def build_index_for_run(run_id: str) -> IndexResponse:
    run = _get_run_or_404(run_id)

    # Index across all docs that have embeddings.
    store_vs = VectorStore(dim=384)
    idx = IndexState(dim=384, store=store_vs)
    count = 0

    for doc_id, emb in run.embeddings.items():
        for chunk_id, vec in emb.vector_by_chunk_id.items():
            vid = emb.vector_id_by_chunk_id[chunk_id]
            store_vs.add(vid, vec, meta={"chunk_id": chunk_id, "doc_id": doc_id})
            idx.chunk_id_by_vector_id[vid] = chunk_id
            idx.doc_id_by_vector_id[vid] = doc_id
            count += 1

    run.index = idx
    mapping_preview = [{"vector_id": vid, "chunk_id": cid} for vid, cid in list(idx.chunk_id_by_vector_id.items())[:20]]
    return IndexResponse(indexed=count, mapping_preview=mapping_preview)


@router.post("/runs/{run_id}/retrieve", response_model=RetrieveResponse)
def retrieve(run_id: str, req: RetrieveRequest) -> RetrieveResponse:
    run = _get_run_or_404(run_id)
    if run.index is None:
        raise HTTPException(status_code=400, detail="index not built; run index step first")

    qv = fake_embed_384(req.query)
    results = run.index.store.search(qv, top_k=req.top_k)

    out: list[RetrieveResult] = []
    for rank, r in enumerate(results, start=1):
        chunk_id = r.meta.get("chunk_id", "")
        doc_id = r.meta.get("doc_id", "")
        chunk_preview = ""
        for c in run.chunks.get(doc_id, []):
            if c.chunk_id == chunk_id:
                chunk_preview = preview_text(c.text)
                break
        out.append(
            RetrieveResult(
                rank=rank,
                score=float(r.score),
                doc_id=doc_id,
                chunk_id=chunk_id,
                vector_id=r.vector_id,
                chunk_preview=chunk_preview,
            )
        )

    return RetrieveResponse(
        query=req.query,
        top_k=req.top_k,
        query_vector_preview=preview_vector(qv),
        results=out,
    )

