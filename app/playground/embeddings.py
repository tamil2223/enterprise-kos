from __future__ import annotations

import hashlib
import math
import re


_TOKEN_RE = re.compile(r"[a-z0-9_]+", flags=re.IGNORECASE)


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def fake_embed_384(text: str) -> list[float]:
    """
    Deterministic fake embedding for demos.

    - 384 dimensions
    - signed hashing of tokens into buckets
    - L2 normalized (so cosine similarity is dot product)
    """
    dim = 384
    v = [0.0] * dim
    toks = _tokens(text)
    if not toks:
        return v

    for tok in toks:
        h = hashlib.sha1(tok.encode("utf-8")).digest()
        idx = int.from_bytes(h[:4], "big") % dim
        sign = -1.0 if (h[4] & 1) else 1.0
        # weight by token length a little to avoid totally flat vectors
        v[idx] += sign * (1.0 + min(len(tok), 12) / 12.0)

    norm = math.sqrt(sum(x * x for x in v))
    if norm == 0.0:
        return v
    return [x / norm for x in v]

