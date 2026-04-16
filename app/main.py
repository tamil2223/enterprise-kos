from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.mcp.gateway import ContextGateway
from app.rag.ingest import TextDocument, chunk_paragraphs, load_corpus_text_files
from app.rag.retrieve import build_index
from app.state import AppState


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    docs = load_corpus_text_files(settings.data_dir)
    chunks: list[TextDocument] = []
    for doc in docs:
        chunks.extend(chunk_paragraphs(doc))

    index = build_index(chunks)
    app.state.kos = AppState(gateway=ContextGateway(settings=settings, index=index))
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Enterprise Knowledge OS (KOS)", version="0.1.0", lifespan=lifespan)
    app.include_router(api_router)
    return app


app = create_app()
