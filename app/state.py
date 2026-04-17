from __future__ import annotations

from dataclasses import dataclass

from app.mcp.gateway import ContextGateway


@dataclass(slots=True)
class AppState:
    gateway: ContextGateway
