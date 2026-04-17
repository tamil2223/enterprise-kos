# Onboarding Guide: Cold-start performance (BluefinRetail)

**Doc ID:** doc_2216_ybn61yl6
**Company:** BluefinRetail
**Owner:** bob (SRE)
**Created:** 2026-04-15

            ## Goal

            Get a developer from clone → running API → inspecting context → running agent pipeline.

            ## Key Concepts

            - Hybrid retrieval agent pipeline hybrid retrieval MCP router LangGraph RBAC FastAPI redaction RBAC.
- Reranker reranker router reranker reranker reranker provenance router provenance reranker.
- FastAPI router provenance Redis hybrid retrieval context gateway context gateway context gateway router MCP LangGraph LangGraph context gateway.
- Trace Kafka BM25 LangGraph context gateway MCP PGVector redaction FastAPI researcher Kafka trace observability.
- Redis BM25 reranker Kafka context budget reranker synthesizer MCP researcher Redis Redis hybrid retrieval redaction.
- FastAPI BM25 observability agent pipeline RBAC FastAPI BM25 hybrid retrieval BM25 researcher MCP Redis.
- Reranker PGVector agent pipeline context gateway MCP FastAPI hybrid retrieval router researcher Kafka.
- MCP MCP redaction redaction provenance LangGraph provenance context budget BM25 LangGraph.
- Observability researcher context budget agent pipeline Redis BM25 context budget synthesizer.
- Reranker LangGraph PGVector Redis provenance provenance redaction synthesizer trace researcher.

            ## Local workflow

            ```bash
# Inspect context selection
curl -s "http://localhost:8000/context?q=mcp%20gateway&top_k=5" | jq

# Run agent pipeline
curl -s -X POST http://localhost:8000/agent/run               -H "Content-Type: application/json"               -d '{"query":"Explain MCP gateway responsibilities"}' | jq
```


            ## FAQ

            - Router RBAC RBAC synthesizer trace context gateway Kafka Kafka.
- BM25 PGVector MCP provenance RBAC Redis redaction FastAPI trace trace.
- Context budget router agent pipeline reranker context gateway redaction FastAPI synthesizer Kafka observability synthesizer.
- Router router BM25 PGVector context gateway Kafka FastAPI BM25 BM25 router researcher.
- Context gateway synthesizer PGVector Kafka Redis MCP trace synthesizer provenance synthesizer redaction.
- Researcher FastAPI PGVector FastAPI PGVector trace FastAPI context budget router MCP BM25 redaction.
- Kafka router MCP context budget router hybrid retrieval redaction context gateway RBAC RBAC LangGraph.
- MCP observability researcher BM25 Redis synthesizer MCP context gateway MCP agent pipeline.
- Hybrid retrieval hybrid retrieval observability context gateway trace redaction PGVector synthesizer provenance synthesizer context gateway observability router context gateway.
- FastAPI FastAPI Kafka LangGraph router PGVector trace hybrid retrieval.



### Appendix 0: 677307d8ee18-0

Reranker context budget router context gateway Redis hybrid retrieval observability PGVector BM25 Kafka BM25 reranker. RBAC agent pipeline agent pipeline LangGraph LangGraph provenance MCP synthesizer BM25 router hybrid retrieval observability context budget hybrid retrieval. PGVector Redis trace Kafka Redis Kafka FastAPI router. Researcher BM25 BM25 RBAC BM25 observability trace provenance hybrid retrieval redaction redaction. Agent pipeline RBAC synthesizer observability FastAPI router router PGVector LangGraph. Synthesizer hybrid retrieval observability researcher LangGraph synthesizer Redis FastAPI Kafka FastAPI Redis agent pipeline hybrid retrieval.

- Provenance MCP observability router FastAPI router Redis LangGraph PGVector synthesizer researcher agent pipeline.
- Agent pipeline hybrid retrieval hybrid retrieval redaction agent pipeline trace observability reranker BM25 router.
- PGVector context budget MCP MCP Redis hybrid retrieval context budget BM25.
- MCP router trace agent pipeline context gateway Kafka FastAPI synthesizer context budget reranker.
- Router redaction Redis agent pipeline router researcher Kafka reranker context gateway synthesizer.
- MCP router context gateway hybrid retrieval trace context gateway context budget hybrid retrieval RBAC MCP RBAC hybrid retrieval LangGraph reranker.
- Researcher FastAPI researcher context budget LangGraph trace redaction LangGraph Redis observability researcher hybrid retrieval.
- Agent pipeline agent pipeline MCP observability BM25 LangGraph synthesizer observability PGVector context budget Redis.

### Appendix 1: 677307d8ee18-1

Researcher synthesizer LangGraph LangGraph observability reranker LangGraph observability trace LangGraph researcher LangGraph RBAC MCP. BM25 reranker RBAC researcher context budget hybrid retrieval BM25 agent pipeline. Context budget agent pipeline researcher synthesizer agent pipeline reranker Kafka redaction FastAPI. Observability FastAPI router MCP BM25 hybrid retrieval BM25 redaction. Reranker MCP Redis LangGraph redaction context budget Kafka Kafka agent pipeline hybrid retrieval synthesizer context budget. Context budget Redis context budget Redis researcher redaction MCP provenance PGVector researcher redaction observability LangGraph agent pipeline.

- Redaction trace context gateway hybrid retrieval observability Kafka Redis PGVector Redis hybrid retrieval.
- Reranker Redis context budget PGVector provenance observability Kafka hybrid retrieval Redis reranker.
- MCP RBAC PGVector Kafka context budget trace synthesizer RBAC agent pipeline researcher PGVector Kafka MCP.
- Reranker context gateway context gateway FastAPI synthesizer context gateway hybrid retrieval context budget router provenance PGVector.
- Kafka provenance MCP PGVector hybrid retrieval PGVector FastAPI Kafka.
- Observability context budget context gateway RBAC router provenance BM25 Redis observability provenance researcher hybrid retrieval.
- BM25 Kafka LangGraph redaction context budget researcher trace MCP LangGraph agent pipeline redaction.
- PGVector synthesizer LangGraph observability PGVector agent pipeline provenance observability Redis synthesizer MCP context gateway agent pipeline reranker.
