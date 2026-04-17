from __future__ import annotations

import hashlib
from dataclasses import dataclass

from app.core.config import Settings
from app.mcp.schemas import ContextItem, Source
from app.rag.retrieve import RetrievalIndex, retrieve_top_k


def _stable_short_id(parts: list[str]) -> str:
    h = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()
    return h[:12]


@dataclass(slots=True)
class ContextGateway:
    settings: Settings
    index: RetrievalIndex

    def build_contexts(self, query: str, top_k: int | None) -> list[ContextItem]:
        k = self.settings.top_k_default if top_k is None else top_k
        ranked = retrieve_top_k(
            query,
            self.index,
            k,
            max_candidates=self.settings.retrieval_max_candidates,
        )

        contexts: list[ContextItem] = []
        total_chars = 0

        seen_text: set[str] = set()
        for r in ranked:
            text = r.doc.text.strip()
            if not text or text in seen_text:
                continue
            seen_text.add(text)

            cid = _stable_short_id([r.doc.source_path, text[:200]])
            item = ContextItem(
                id=cid,
                title=r.doc.title,
                text=text,
                source=r.doc.source_path,
                score=float(r.score),
                metadata={
                    "semantic_score": float(r.semantic_score),
                    "lexical_score": float(r.lexical_score),
                },
            )

            projected = total_chars + len(item.text)
            if projected > self.settings.context_max_chars and contexts:
                break
            contexts.append(item)
            total_chars = projected

        return contexts

    def to_sources(self, contexts: list[ContextItem]) -> list[Source]:
        return [
            Source(id=c.id, title=c.title, source=c.source, score=c.score)
            for c in contexts
        ]
