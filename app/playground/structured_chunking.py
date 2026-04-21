from __future__ import annotations

import re
from dataclasses import dataclass

from app.playground.chunking import Chunk


@dataclass(frozen=True, slots=True)
class SectionSpan:
    section_id: str
    title: str
    heading_path: str
    start_char: int
    end_char: int
    text: str


_MD_ATX = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$")
_ITEM_LINE = re.compile(
    r"^\s*(?:(?:ITEM|Item)\s*\d+[A-Z]?|(?:PART|Part)\s*\d+|[IVXLC]+\.)\s+.{3,}$"
)
_RISK_LINE = re.compile(r"^\s*(RISK\s+FACTORS|Risk\s+Factors)\s*$", re.IGNORECASE)


def _norm_ws(s: str) -> str:
    return " ".join(s.split()).strip()


def _split_sentences(text: str) -> list[str]:
    """
    Lightweight sentence splitter (good enough for playground v2).

    - Prefers punctuation boundaries (.?!)
    - Falls back to single-line units if no punctuation is present
    """
    t = text.strip()
    if not t:
        return []

    parts = re.split(r"(?<=[.!?])\s+", t)
    out: list[str] = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(parts) == 1 and p == t and "\n" in p:
            # Multiline "paragraph" with no punctuation: split by lines.
            for line in p.splitlines():
                line = line.strip()
                if line:
                    out.append(line)
            return out
        out.append(p)
    return out


def _split_sentences_with_spans(rel: str) -> list[tuple[str, int, int]]:
    """
    Like `_split_sentences`, but also returns [start, end) offsets into `rel`.

    Offsets are best-effort substring matches scanned left-to-right.
    """
    sents = _split_sentences(rel)
    if not sents:
        return []

    cursor = 0
    out: list[tuple[str, int, int]] = []
    for s in sents:
        idx = rel.find(s, cursor)
        if idx < 0:
            idx = rel.find(s)
        if idx < 0:
            # Last resort: treat as empty span at cursor
            idx = cursor
        start = idx
        end = start + len(s)
        out.append((s, start, end))
        cursor = end
    return out


def _title_case_heading(line: str) -> str:
    s = line.strip()
    if len(s) <= 80:
        return s
    return s[:77].rstrip() + "…"


def parse_sections(*, text: str, doc_id: str, content_type: str) -> list[SectionSpan]:
    """
    Best-effort structure extraction.

    v2 rules:
    - Markdown: split on ATX headings (# .. ######)
    - Plaintext: SEC-ish / outline-ish cues + simple "title block" heuristics
    - Fallback: single section covering the whole document
    """
    if content_type == "text/markdown":
        return _parse_md_atx_sections(text=text, doc_id=doc_id)

    if content_type == "text/plain":
        sections = _parse_plain_outline_sections(text=text, doc_id=doc_id)
        if len(sections) >= 2:
            return sections

        kb = _parse_plain_kb_title_blocks(text=text, doc_id=doc_id)
        if len(kb) >= 2:
            return kb

        return [
            SectionSpan(
                section_id=f"{doc_id}#sec-root",
                title="Document",
                heading_path="Document",
                start_char=0,
                end_char=len(text),
                text=text,
            )
        ]

    # Unknown content types shouldn't happen in v1, but keep safe behavior.
    return [
        SectionSpan(
            section_id=f"{doc_id}#sec-root",
            title="Document",
            heading_path="Document",
            start_char=0,
            end_char=len(text),
            text=text,
        )
    ]


def _parse_md_atx_sections(*, text: str, doc_id: str) -> list[SectionSpan]:
    lines = text.splitlines(keepends=True)
    headings: list[tuple[int, int, str, str]] = []  # (line_idx, level, title, path)

    stack: list[tuple[int, str]] = []  # (level, title)

    for i, line in enumerate(lines):
        m = _MD_ATX.match(line)
        if not m:
            continue
        level = len(m.group(1))
        title = _norm_ws(m.group(2))
        if not title:
            continue

        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))

        path = " > ".join(t for _, t in stack)
        headings.append((i, level, title, path))

    if not headings:
        return [
            SectionSpan(
                section_id=f"{doc_id}#sec-root",
                title="Document",
                heading_path="Document",
                start_char=0,
                end_char=len(text),
                text=text,
            )
        ]

    spans: list[SectionSpan] = []
    for hi, (line_idx, _level, title, path) in enumerate(headings):
        start_line = line_idx
        end_line = headings[hi + 1][0] if hi + 1 < len(headings) else len(lines)

        start_char = sum(len(lines[j]) for j in range(0, start_line))
        end_char = sum(len(lines[j]) for j in range(0, end_line))
        heading_line = lines[line_idx]
        body_start_char = start_char + len(heading_line)
        body = text[body_start_char:end_char]

        sec_slug = re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")[:48] or "section"
        section_id = f"{doc_id}#sec-{hi}-{sec_slug}"

        spans.append(
            SectionSpan(
                section_id=section_id,
                title=title,
                heading_path=path,
                start_char=body_start_char,
                end_char=end_char,
                text=body,
            )
        )

    return spans


def _parse_plain_outline_sections(*, text: str, doc_id: str) -> list[SectionSpan]:
    lines = text.splitlines(keepends=True)
    markers: list[tuple[int, str]] = []

    for i, line in enumerate(lines):
        raw = line.strip()
        if not raw:
            continue
        if _ITEM_LINE.match(raw) or _RISK_LINE.match(raw):
            markers.append((i, _title_case_heading(raw)))

    if len(markers) < 2:
        return []

    spans: list[SectionSpan] = []
    for mi, (line_idx, title) in enumerate(markers):
        start_line = line_idx
        end_line = markers[mi + 1][0] if mi + 1 < len(markers) else len(lines)

        start_char = sum(len(lines[j]) for j in range(0, start_line))
        end_char = sum(len(lines[j]) for j in range(0, end_line))
        body = text[start_char:end_char]

        path = title
        sec_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "section"
        section_id = f"{doc_id}#sec-{mi}-{sec_slug}"

        spans.append(
            SectionSpan(
                section_id=section_id,
                title=title,
                heading_path=path,
                start_char=start_char,
                end_char=end_char,
                text=body,
            )
        )

    return spans


def _parse_plain_kb_title_blocks(*, text: str, doc_id: str) -> list[SectionSpan]:
    """
    Heuristic "knowledge article" splitter:
    a short title line followed by a blank line, starting a section.
    """
    lines = text.splitlines(keepends=True)
    starts: list[int] = []

    for i in range(len(lines) - 2):
        t0 = lines[i].strip()
        t1 = lines[i + 1].strip()
        if not t0 or len(t0) > 80:
            continue
        if t1 != "":
            continue
        # Next non-empty line should exist and not be another tiny title-with-blank pattern immediately.
        nxt = ""
        for j in range(i + 2, len(lines)):
            if lines[j].strip() != "":
                nxt = lines[j].strip()
                break
        if not nxt:
            continue
        starts.append(i)

    # De-dupe consecutive starts (rare)
    dedup: list[int] = []
    for s in starts:
        if not dedup or s > dedup[-1]:
            dedup.append(s)

    if len(dedup) < 2:
        return []

    spans: list[SectionSpan] = []
    for si, start_line in enumerate(dedup):
        end_line = dedup[si + 1] if si + 1 < len(dedup) else len(lines)
        start_char = sum(len(lines[j]) for j in range(0, start_line))
        end_char = sum(len(lines[j]) for j in range(0, end_line))
        body = text[start_char:end_char]
        title = _title_case_heading(lines[start_line])
        path = title
        sec_slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:48] or "section"
        section_id = f"{doc_id}#sec-{si}-{sec_slug}"
        spans.append(
            SectionSpan(
                section_id=section_id,
                title=title,
                heading_path=path,
                start_char=start_char,
                end_char=end_char,
                text=body,
            )
        )

    return spans


def _build_context_header(*, source_name: str, heading_path: str) -> str:
    doc = _norm_ws(source_name) or "document"
    hp = _norm_ws(heading_path) or "section"
    return f"doc: {doc} | path: {hp}"


def _overlap_tail_sentences(prev_sentences: list[str], overlap: int) -> list[str]:
    if overlap <= 0 or not prev_sentences:
        return []
    picked: list[str] = []
    total = 0
    for s in reversed(prev_sentences):
        picked.append(s)
        add = len(s) if total == 0 else len(s) + 1
        total += add
        if total >= overlap:
            break
    picked.reverse()
    return picked


def chunk_structured_document(
    *,
    text: str,
    doc_id: str,
    source_name: str,
    content_type: str,
    target_chunk_chars: int,
    max_chunk_chars: int,
    overlap: int,
) -> list[Chunk]:
    if target_chunk_chars <= 0:
        raise ValueError("target_chunk_chars must be > 0")
    if max_chunk_chars < target_chunk_chars:
        raise ValueError("max_chunk_chars must be >= target_chunk_chars")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    if overlap >= target_chunk_chars:
        raise ValueError("overlap must be < target_chunk_chars")

    sections = parse_sections(text=text, doc_id=doc_id, content_type=content_type)

    chunks: list[Chunk] = []
    global_i = 0

    for sec in sections:
        sec_body = sec.text
        # Strip leading/trailing whitespace for unitization, but keep absolute offsets anchored to sec span.
        # We compute sentence offsets relative to sec_body, then shift by sec.start_char.
        rel = sec_body.strip("\n")
        rel_start_in_sec = sec_body.find(rel) if rel else 0
        if rel_start_in_sec < 0:
            rel_start_in_sec = 0

        abs_sec_text_start = sec.start_char + rel_start_in_sec
        units = _split_sentences_with_spans(rel)
        if not units:
            continue

        sec_chunk_idx = 0

        # Pack units into chunks within this section.
        buf: list[str] = []
        buf_sentences: list[str] = []
        buf_spans: list[tuple[int, int]] = []
        buf_len = 0

        def flush_buf(force: bool = False) -> None:
            nonlocal buf, buf_sentences, buf_spans, buf_len, global_i, sec_chunk_idx
            if not buf:
                return
            joined = " ".join(buf)
            joined = joined.strip()
            if not joined:
                buf = []
                buf_sentences = []
                buf_spans = []
                buf_len = 0
                return

            # Enforce max by dropping whole leading sentences until under max (best-effort).
            sent_list = buf_sentences[:]
            spans_list = buf_spans[:]
            j_text = joined
            while len(j_text) > max_chunk_chars and len(sent_list) > 1:
                sent_list = sent_list[1:]
                spans_list = spans_list[1:]
                j_text = " ".join(sent_list).strip()

            abs_start = abs_sec_text_start + spans_list[0][0]
            abs_end = abs_sec_text_start + spans_list[-1][1]

            header = _build_context_header(source_name=source_name, heading_path=sec.heading_path)
            embed_text = f"{header}\n\n{j_text}"

            chunks.append(
                Chunk(
                    chunk_id=f"{doc_id}#chunk-{global_i}",
                    doc_id=doc_id,
                    chunk_index=global_i,
                    start_char=abs_start,
                    end_char=abs_end,
                    text=j_text,
                    embed_text=embed_text,
                    strategy="structured",
                    section_id=sec.section_id,
                    section_title=sec.title,
                    heading_path=sec.heading_path,
                    source_name=source_name,
                    section_chunk_index=sec_chunk_idx,
                )
            )
            global_i += 1
            sec_chunk_idx += 1

            tail = _overlap_tail_sentences(sent_list, overlap)
            # Re-map overlap tail to spans: take suffix of sentences list aligned with spans_list tail.
            if not tail:
                buf = []
                buf_sentences = []
                buf_spans = []
                buf_len = 0
            else:
                k = len(sent_list) - len(tail)
                buf = tail[:]
                buf_sentences = tail[:]
                buf_spans = spans_list[k:]
                buf_len = sum(len(x) + 1 for x in buf) - (1 if buf else 0)

            # If forced and still too big, allow empty buffer
            if force and buf_len > max_chunk_chars:
                buf = []
                buf_sentences = []
                buf_spans = []
                buf_len = 0

        for u, us, ue in units:
            u = u.strip()
            if not u:
                continue

            add_len = len(u) + (1 if buf_len else 0)
            if buf_len + add_len > target_chunk_chars and buf:
                flush_buf(force=False)

            # If a single sentence exceeds max, flush it alone (can't split).
            if len(u) > max_chunk_chars:
                flush_buf(force=True)
                abs_start = abs_sec_text_start + us
                abs_end = abs_sec_text_start + ue
                chunks.append(
                    Chunk(
                        chunk_id=f"{doc_id}#chunk-{global_i}",
                        doc_id=doc_id,
                        chunk_index=global_i,
                        start_char=abs_start,
                        end_char=abs_end,
                        text=u,
                        embed_text=f"{_build_context_header(source_name=source_name, heading_path=sec.heading_path)}\n\n{u}",
                        strategy="structured",
                        section_id=sec.section_id,
                        section_title=sec.title,
                        heading_path=sec.heading_path,
                        source_name=source_name,
                        section_chunk_index=sec_chunk_idx,
                    )
                )
                global_i += 1
                sec_chunk_idx += 1
                buf = []
                buf_sentences = []
                buf_spans = []
                buf_len = 0
                continue

            if buf_len + add_len > max_chunk_chars and buf:
                flush_buf(force=True)

            buf.append(u)
            buf_sentences.append(u)
            buf_spans.append((us, ue))
            buf_len += add_len

        flush_buf(force=True)

    return chunks
