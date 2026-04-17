from __future__ import annotations

import math
import re
from dataclasses import dataclass

from app.rag.ingest import TextDocument


_TOKEN_RE = re.compile(r"[a-z0-9_]+", flags=re.IGNORECASE)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


@dataclass(frozen=True, slots=True)
class RetrievedChunk:
    doc: TextDocument
    semantic_score: float
    lexical_score: float
    score: float


@dataclass(frozen=True, slots=True)
class RetrievalIndex:
    chunks: list[TextDocument]
    doc_tokens: list[list[str]]
    doc_token_sets: list[set[str]]
    df: dict[str, int]
    postings: dict[str, list[int]]


def _tf(term: str, tokens: list[str]) -> float:
    if not tokens:
        return 0.0
    return tokens.count(term) / len(tokens)


def build_index(chunks: list[TextDocument]) -> RetrievalIndex:
    doc_tokens: list[list[str]] = []
    doc_token_sets: list[set[str]] = []
    df: dict[str, int] = {}
    postings: dict[str, list[int]] = {}

    for i, c in enumerate(chunks):
        toks = tokenize(c.text)
        doc_tokens.append(toks)
        s = set(toks)
        doc_token_sets.append(s)
        for t in s:
            df[t] = df.get(t, 0) + 1
            postings.setdefault(t, []).append(i)

    return RetrievalIndex(
        chunks=chunks,
        doc_tokens=doc_tokens,
        doc_token_sets=doc_token_sets,
        df=df,
        postings=postings,
    )


def hybrid_score(
    *,
    query_tokens: list[str],
    doc: TextDocument,
    doc_tokens: list[str],
    doc_token_set: set[str],
    df: dict[str, int],
    corpus_size: int,
) -> RetrievedChunk:
    if not query_tokens or not doc_tokens:
        return RetrievedChunk(doc=doc, semantic_score=0.0, lexical_score=0.0, score=0.0)

    # v1 "semantic" proxy: token overlap cosine similarity (cheap + deterministic)
    q_set = set(query_tokens)
    overlap = len(q_set & doc_token_set)
    denom = math.sqrt(len(q_set)) * math.sqrt(len(doc_token_set))
    semantic = overlap / denom if denom else 0.0

    # v1 "BM25-ish" proxy: sum of TF-IDF style weights for query terms
    lexical = 0.0
    N = max(corpus_size, 1)
    for term in q_set:
        tf = _tf(term, doc_tokens)
        if tf <= 0:
            continue
        dfi = max(df.get(term, 1), 1)
        idf = math.log((N + 1) / (dfi + 1)) + 1.0
        lexical += tf * idf

    # Simple fusion
    score = 0.65 * semantic + 0.35 * (lexical / (10.0 + lexical))
    return RetrievedChunk(doc=doc, semantic_score=semantic, lexical_score=lexical, score=score)


def _candidate_indices(index: RetrievalIndex, query_tokens: list[str], max_candidates: int) -> list[int]:
    q_terms = sorted(set(query_tokens), key=lambda t: index.df.get(t, 10**9))
    if not q_terms:
        return list(range(len(index.chunks)))[:max_candidates]

    candidates: set[int] = set()
    for t in q_terms:
        for i in index.postings.get(t, []):
            candidates.add(i)
            if len(candidates) >= max_candidates:
                return list(candidates)

    # If we got too few candidates (rare query terms), fall back to a larger pool.
    if len(candidates) < min(200, max_candidates):
        return list(range(len(index.chunks)))[:max_candidates]

    return list(candidates)


def retrieve_top_k(query: str, index: RetrievalIndex, top_k: int, max_candidates: int) -> list[RetrievedChunk]:
    q_tokens = tokenize(query)
    cand = _candidate_indices(index, q_tokens, max_candidates=max_candidates)

    ranked: list[RetrievedChunk] = []
    N = len(index.chunks)
    for i in cand:
        doc = index.chunks[i]
        ranked.append(
            hybrid_score(
                query_tokens=q_tokens,
                doc=doc,
                doc_tokens=index.doc_tokens[i],
                doc_token_set=index.doc_token_sets[i],
                df=index.df,
                corpus_size=N,
            )
        )

    ranked.sort(key=lambda r: r.score, reverse=True)
    return ranked[: max(top_k, 0)]
