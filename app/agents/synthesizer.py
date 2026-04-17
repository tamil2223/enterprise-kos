from __future__ import annotations

from app.mcp.schemas import ContextItem


def synthesize(query: str, contexts: list[ContextItem]) -> str:
    if not contexts:
        return (
            "I do not have enough grounded context in the local corpus to answer that yet. "
            "Try adding `.txt` documents under `data/corpus/` and re-run the server."
        )

    bullets: list[str] = []
    for i, c in enumerate(contexts, start=1):
        snippet = c.text.strip().replace("\n", " ")
        if len(snippet) > 320:
            snippet = snippet[:320].rstrip() + "…"
        bullets.append(f"{i}) ({c.source}) {snippet}")

    joined = "\n".join(bullets)
    return (
        f"Answer (grounded on retrieved contexts):\n"
        f"- Query: {query.strip()}\n"
        f"- Key evidence:\n{joined}\n"
        f"- Note: v1 uses a lightweight hybrid retrieval proxy (overlap + lexical weighting)."
    )
