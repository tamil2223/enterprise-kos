from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class SearchResult:
    vector_id: str
    score: float
    meta: dict[str, Any]


def _l2_normalize(v: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0.0:
        return [0.0 for _ in v]
    return [x / norm for x in v]


class VectorStore:
    def __init__(self, *, dim: int):
        if dim <= 0:
            raise ValueError("dim must be > 0")
        self.dim = dim
        self._vector_ids: list[str] = []
        self._vectors: list[list[float]] = []
        self._metas: list[dict[str, Any]] = []

    def add(self, vector_id: str, vector: list[float], *, meta: dict[str, Any]) -> None:
        if len(vector) != self.dim:
            raise ValueError(f"vector must have dim={self.dim}")
        self._vector_ids.append(vector_id)
        self._vectors.append(_l2_normalize(vector))
        # Store a shallow copy to avoid surprising external mutation.
        self._metas.append(dict(meta))

    def search(self, query_vector: list[float], *, top_k: int) -> list[SearchResult]:
        if len(query_vector) != self.dim:
            raise ValueError(f"query_vector must have dim={self.dim}")
        if top_k <= 0:
            return []
        q = _l2_normalize(query_vector)

        scored: list[tuple[float, int]] = []
        for i, v in enumerate(self._vectors):
            # Cosine similarity once normalized
            score = sum(a * b for a, b in zip(q, v))
            scored.append((float(score), i))

        scored.sort(key=lambda t: t[0], reverse=True)
        out: list[SearchResult] = []
        for score, i in scored[:top_k]:
            out.append(
                SearchResult(
                    vector_id=self._vector_ids[i],
                    score=score,
                    meta=dict(self._metas[i]),
                )
            )
        return out

