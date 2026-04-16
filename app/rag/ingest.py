from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TextDocument:
    doc_id: str
    title: str
    source_path: str
    text: str


def _read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_corpus_text_files(data_dir: Path) -> list[TextDocument]:
    if not data_dir.exists():
        return []

    docs: list[TextDocument] = []
    for path in sorted(data_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".txt", ".md"}:
            continue

        text = _read_text_file(path)
        rel = str(path.as_posix())
        docs.append(
            TextDocument(
                doc_id=rel,
                title=path.stem.replace("_", " ").replace("-", " ").title(),
                source_path=rel,
                text=text,
            )
        )

    return docs


def chunk_paragraphs(doc: TextDocument, max_chunk_chars: int = 1200) -> list[TextDocument]:
    paragraphs = [p.strip() for p in doc.text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: list[TextDocument] = []
    buf: list[str] = []
    buf_len = 0
    chunk_idx = 0

    def flush() -> None:
        nonlocal buf, buf_len, chunk_idx
        if not buf:
            return
        chunk_text = "\n\n".join(buf).strip()
        chunks.append(
            TextDocument(
                doc_id=f"{doc.doc_id}#chunk-{chunk_idx}",
                title=doc.title,
                source_path=doc.source_path,
                text=chunk_text,
            )
        )
        chunk_idx += 1
        buf = []
        buf_len = 0

    for p in paragraphs:
        if buf_len + len(p) + 2 > max_chunk_chars:
            flush()
        buf.append(p)
        buf_len += len(p) + 2
    flush()

    return chunks
