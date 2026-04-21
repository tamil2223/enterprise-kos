from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Chunk:
    chunk_id: str
    doc_id: str
    chunk_index: int
    start_char: int
    end_char: int
    text: str
    # Optional v2 fields (structured chunking + embed-time context)
    embed_text: str | None = None
    strategy: str = "window"
    section_id: str | None = None
    section_title: str | None = None
    heading_path: str | None = None
    source_name: str | None = None
    section_chunk_index: int | None = None


def chunk_text_window(*, text: str, chunk_size: int, overlap: int, doc_id: str) -> list[Chunk]:
    """
    Sliding-window chunking over raw text (character-based).

    `overlap` is the number of characters shared between adjacent chunks.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be < chunk_size")

    if not text:
        return []

    chunks: list[Chunk] = []
    i = 0
    start = 0
    n = len(text)
    step = chunk_size - overlap

    while start < n:
        end = min(start + chunk_size, n)
        chunk_text = text[start:end]
        chunks.append(
            Chunk(
                chunk_id=f"{doc_id}#chunk-{i}",
                doc_id=doc_id,
                chunk_index=i,
                start_char=start,
                end_char=end,
                text=chunk_text,
                embed_text=chunk_text,
                strategy="window",
                section_id=f"{doc_id}#sec-root",
                section_title="Document",
                heading_path="Document",
                source_name=None,
                section_chunk_index=i,
            )
        )
        i += 1
        if end >= n:
            break
        start += step

    return chunks

