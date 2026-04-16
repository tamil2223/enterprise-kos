from __future__ import annotations

from app.agents.researcher import research
from app.agents.router import route_query
from app.agents.synthesizer import synthesize
from app.mcp.gateway import ContextGateway
from app.mcp.schemas import AgentRunResponse, AgentStep, ContextItem


def run_agent_pipeline(query: str, gateway: ContextGateway) -> AgentRunResponse:
    route = route_query(query)
    steps: list[AgentStep] = []

    steps.append(
        AgentStep(
            name="router",
            input=query.strip(),
            output=f"route={route}",
        )
    )

    contexts: list[ContextItem]
    if route == "needs_retrieval":
        contexts = research(query=query, gateway=gateway, top_k=None)
        steps.append(
            AgentStep(
                name="researcher",
                input=query.strip(),
                output=f"retrieved_contexts={len(contexts)}",
            )
        )
    else:
        contexts = []
        steps.append(
            AgentStep(
                name="researcher",
                input=query.strip(),
                output="skipped_retrieval_for_direct_route",
            )
        )

    final = synthesize(query=query, contexts=contexts)
    steps.append(
        AgentStep(
            name="synthesizer",
            input=f"contexts={len(contexts)}",
            output=final[:800] + ("…" if len(final) > 800 else ""),
        )
    )

    return AgentRunResponse(final=final, steps=steps, contexts=contexts)
