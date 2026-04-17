from __future__ import annotations

import re


_GREETING_RE = re.compile(r"\b(hi|hello|hey)\b", flags=re.IGNORECASE)


def route_query(query: str) -> str:
    q = query.strip()
    if _GREETING_RE.search(q):
        return "direct_answer"
    return "needs_retrieval"
