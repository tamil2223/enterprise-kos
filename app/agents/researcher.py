from __future__ import annotations

from app.mcp.gateway import ContextGateway
from app.mcp.schemas import ContextItem


def research(query: str, gateway: ContextGateway, top_k: int | None) -> list[ContextItem]:
    return gateway.build_contexts(query=query, top_k=top_k)
