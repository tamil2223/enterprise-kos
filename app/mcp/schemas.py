from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ContextItem(BaseModel):
    id: str
    title: str
    text: str
    source: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class Source(BaseModel):
    id: str
    title: str
    source: str
    score: float


class QueryRequest(BaseModel):
    query: str
    top_k: int | None = None
    filters: dict[str, Any] | None = None


class QueryResponse(BaseModel):
    answer: str
    contexts: list[ContextItem]
    sources: list[Source]


class AgentRunRequest(BaseModel):
    query: str
    mode: str | None = "default"


class AgentStep(BaseModel):
    name: str
    input: str
    output: str


class AgentRunResponse(BaseModel):
    final: str
    steps: list[AgentStep]
    contexts: list[ContextItem]
