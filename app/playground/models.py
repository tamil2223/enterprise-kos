from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel

from app.playground.chunking import Chunk
from app.playground.vector_store import VectorStore


@dataclass(slots=True)
class Document:
    doc_id: str
    name: str
    content_type: Literal["text/plain", "text/markdown"]
    text: str


@dataclass(slots=True)
class EmbeddingState:
    dim: int
    vector_by_chunk_id: dict[str, list[float]] = field(default_factory=dict)
    vector_id_by_chunk_id: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class IndexState:
    dim: int
    store: VectorStore
    chunk_id_by_vector_id: dict[str, str] = field(default_factory=dict)
    doc_id_by_vector_id: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class RunState:
    run_id: str
    created_at: float
    documents: dict[str, Document] = field(default_factory=dict)
    chunks: dict[str, list[Chunk]] = field(default_factory=dict)  # doc_id -> chunks
    chunk_params: dict[str, tuple[int, int]] = field(default_factory=dict)  # doc_id -> (chunk_size, overlap)
    embeddings: dict[str, EmbeddingState] = field(default_factory=dict)  # doc_id -> embeddings
    index: IndexState | None = None


class CreateRunResponse(BaseModel):
    run_id: str


class DocumentInfo(BaseModel):
    doc_id: str
    name: str
    content_type: str
    size_chars: int


class ListDocumentsResponse(BaseModel):
    documents: list[DocumentInfo]


class RunSummaryResponse(BaseModel):
    run_id: str
    documents_count: int
    chunked_docs_count: int
    embedded_docs_count: int
    indexed_vectors_count: int

    has_documents: bool
    has_chunks: bool
    has_embeddings: bool
    has_index: bool


class ChunkRequest(BaseModel):
    doc_id: str
    chunk_size: int
    overlap: int


class ChunkInfo(BaseModel):
    chunk_id: str
    doc_id: str
    chunk_index: int
    start_char: int
    end_char: int
    text_preview: str


class ChunkResponse(BaseModel):
    doc_id: str
    chunk_size: int
    overlap: int
    chunks: list[ChunkInfo]


class EmbedRequest(BaseModel):
    doc_id: str


class EmbedResponse(BaseModel):
    doc_id: str
    dim: int
    mapping_preview: list[dict[str, str]]
    vectors_preview: list[list[float]]


class IndexResponse(BaseModel):
    indexed: int
    mapping_preview: list[dict[str, str]]


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5


class RetrieveResult(BaseModel):
    rank: int
    score: float
    doc_id: str
    chunk_id: str
    vector_id: str
    chunk_preview: str


class RetrieveResponse(BaseModel):
    query: str
    top_k: int
    query_vector_preview: list[float]
    results: list[RetrieveResult]


def preview_text(text: str, max_chars: int = 240) -> str:
    t = " ".join(text.strip().split())
    if len(t) <= max_chars:
        return t
    return t[:max_chars].rstrip() + "…"


def preview_vector(v: list[float], max_dims: int = 16) -> list[float]:
    return [float(x) for x in v[:max_dims]]

