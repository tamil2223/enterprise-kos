from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from app.agents.runner import run_agent_pipeline
from app.agents.synthesizer import synthesize
from app.mcp.schemas import AgentRunRequest, AgentRunResponse, QueryRequest, QueryResponse
from app.state import AppState


router = APIRouter()


def get_state(request: Request) -> AppState:
    state = getattr(request.app.state, "kos", None)
    if state is None:
        raise HTTPException(status_code=500, detail="App state is not initialized")
    return state


@router.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/context")
def get_context(q: str, top_k: int | None = None, state: AppState = Depends(get_state)) -> dict:
    contexts = state.gateway.build_contexts(query=q, top_k=top_k)
    return {"contexts": contexts}


@router.post("/query", response_model=QueryResponse)
def post_query(req: QueryRequest, state: AppState = Depends(get_state)) -> QueryResponse:
    top_k = req.top_k
    contexts = state.gateway.build_contexts(query=req.query, top_k=top_k)
    answer = synthesize(query=req.query, contexts=contexts)
    sources = state.gateway.to_sources(contexts)
    return QueryResponse(answer=answer, contexts=contexts, sources=sources)


@router.post("/agent/run", response_model=AgentRunResponse)
def post_agent_run(req: AgentRunRequest, state: AppState = Depends(get_state)) -> AgentRunResponse:
    # `mode` is accepted for forward compatibility; v1 ignores it beyond tracing in steps.
    _ = req.mode
    return run_agent_pipeline(query=req.query, gateway=state.gateway)
