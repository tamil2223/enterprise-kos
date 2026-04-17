# Incident Postmortem: Cold-start performance (QuantaGov)

**Doc ID:** doc_7941_uzi7vrry
**Company:** QuantaGov
**Owner:** erin (AI Apps)
**Created:** 2026-04-15

            ## Summary

            SEV-2 incident `INC-9630` impacted responses produced by the agent pipeline (Router → Researcher → Synthesizer).
            Users observed inconsistent citations and context truncation under load.

            ## Impact

            - BM25 provenance agent pipeline LangGraph trace context budget router FastAPI MCP.
- Synthesizer PGVector MCP provenance RBAC reranker trace router Kafka provenance trace hybrid retrieval.
- Context gateway hybrid retrieval redaction RBAC router FastAPI observability LangGraph.
- RBAC observability PGVector router synthesizer MCP FastAPI RBAC agent pipeline observability MCP.
- Researcher researcher FastAPI PGVector Redis redaction agent pipeline LangGraph reranker Redis.

            ## Root Cause

            Redis RBAC provenance context budget PGVector researcher provenance router RBAC redaction FastAPI. Redis reranker reranker provenance observability BM25 provenance MCP researcher context gateway Redis redaction researcher redaction. FastAPI Redis trace router LangGraph context budget BM25 context gateway trace RBAC LangGraph BM25 router observability. RBAC observability synthesizer agent pipeline synthesizer reranker agent pipeline agent pipeline FastAPI BM25 Kafka FastAPI router router. PGVector provenance Redis RBAC Redis synthesizer LangGraph MCP agent pipeline synthesizer.

            ## Detection

            Kafka synthesizer context budget context gateway context gateway LangGraph RBAC Kafka provenance. Hybrid retrieval PGVector observability researcher agent pipeline observability context budget provenance trace. Provenance Redis LangGraph Redis researcher MCP provenance observability agent pipeline researcher.

            ## Resolution

            - Provenance provenance LangGraph trace trace FastAPI BM25 researcher hybrid retrieval researcher agent pipeline.
- Reranker LangGraph reranker LangGraph BM25 reranker router provenance context budget trace.
- Context budget Redis PGVector trace router hybrid retrieval trace synthesizer LangGraph context budget reranker provenance Kafka synthesizer.
- Redaction FastAPI Kafka LangGraph observability hybrid retrieval LangGraph PGVector redaction trace.
- Observability Kafka context gateway MCP PGVector PGVector FastAPI trace observability hybrid retrieval.
- Observability provenance MCP Kafka agent pipeline context gateway trace router agent pipeline.

            ## Follow-ups

            - Redis reranker reranker Redis context budget redaction LangGraph context gateway trace researcher.
- BM25 reranker observability trace PGVector redaction BM25 LangGraph Redis provenance RBAC BM25 observability researcher.
- PGVector RBAC observability BM25 router RBAC MCP provenance.
- Context gateway Kafka observability Kafka reranker BM25 RBAC observability reranker Redis redaction PGVector provenance.
- Router context gateway BM25 MCP researcher hybrid retrieval provenance MCP BM25 Kafka hybrid retrieval reranker redaction.
- Router observability PGVector context gateway router BM25 agent pipeline LangGraph.
- Agent pipeline observability RBAC PGVector MCP context gateway BM25 context gateway researcher provenance provenance RBAC.
- Reranker agent pipeline LangGraph BM25 Redis BM25 router PGVector.



### Appendix 0: 8e55cfdcf592-0

Context gateway provenance Redis RBAC FastAPI agent pipeline hybrid retrieval researcher. Agent pipeline agent pipeline MCP provenance agent pipeline MCP BM25 redaction. Reranker agent pipeline researcher Redis BM25 LangGraph agent pipeline context budget. Hybrid retrieval Redis observability context budget MCP hybrid retrieval PGVector context budget FastAPI router reranker reranker synthesizer. Redaction BM25 Kafka LangGraph RBAC Kafka BM25 reranker PGVector redaction. BM25 context budget RBAC trace RBAC synthesizer observability RBAC BM25 redaction FastAPI.

- Hybrid retrieval LangGraph Kafka context gateway LangGraph Kafka provenance redaction synthesizer context budget router.
- Context gateway FastAPI synthesizer Redis LangGraph reranker PGVector context gateway provenance.
- PGVector hybrid retrieval provenance MCP router observability synthesizer context budget observability LangGraph reranker agent pipeline Redis.
- PGVector Kafka reranker hybrid retrieval reranker agent pipeline synthesizer Redis context budget hybrid retrieval.
- Hybrid retrieval LangGraph hybrid retrieval LangGraph agent pipeline provenance BM25 hybrid retrieval.
- Researcher router FastAPI researcher observability PGVector LangGraph RBAC hybrid retrieval.
- BM25 router MCP Kafka MCP Kafka observability MCP provenance context budget observability researcher.
- Redaction context gateway synthesizer trace hybrid retrieval context gateway MCP FastAPI hybrid retrieval.

### Appendix 1: 8e55cfdcf592-1

Reranker agent pipeline synthesizer agent pipeline synthesizer provenance LangGraph PGVector trace. MCP context gateway trace context gateway synthesizer hybrid retrieval router researcher. LangGraph context gateway trace observability reranker provenance observability MCP BM25 Redis router synthesizer synthesizer. Router PGVector trace MCP observability researcher redaction redaction router synthesizer FastAPI context gateway reranker. Agent pipeline trace context gateway LangGraph agent pipeline redaction Kafka hybrid retrieval context budget MCP. Redaction agent pipeline context gateway agent pipeline FastAPI FastAPI observability provenance Redis redaction context gateway MCP context gateway BM25.

- Synthesizer reranker redaction router observability router PGVector provenance redaction researcher.
- Context gateway provenance trace Redis redaction redaction synthesizer researcher reranker context budget redaction Kafka.
- Synthesizer BM25 LangGraph Kafka Redis context budget context budget reranker agent pipeline MCP router PGVector agent pipeline trace.
- Synthesizer FastAPI hybrid retrieval hybrid retrieval context budget MCP observability trace.
- Provenance researcher context budget RBAC reranker BM25 researcher MCP MCP trace synthesizer MCP.
- FastAPI agent pipeline Kafka context gateway PGVector reranker PGVector observability Redis synthesizer hybrid retrieval.
- MCP hybrid retrieval synthesizer researcher MCP context gateway trace observability.
- Researcher agent pipeline FastAPI MCP FastAPI PGVector redaction trace PGVector LangGraph redaction LangGraph.

### Appendix 2: 8e55cfdcf592-2

FastAPI trace FastAPI MCP provenance reranker FastAPI trace redaction MCP provenance context budget hybrid retrieval RBAC. RBAC provenance observability provenance router Kafka observability hybrid retrieval BM25 RBAC researcher. FastAPI context budget LangGraph Redis researcher synthesizer LangGraph researcher synthesizer hybrid retrieval hybrid retrieval. Trace observability reranker context gateway hybrid retrieval MCP hybrid retrieval LangGraph RBAC router. Researcher Kafka router LangGraph BM25 Kafka FastAPI context budget context budget. Redis FastAPI LangGraph observability FastAPI RBAC observability RBAC Kafka.

- Context budget context gateway BM25 hybrid retrieval LangGraph context gateway observability RBAC researcher.
- Kafka FastAPI redaction reranker Kafka observability Kafka LangGraph Redis.
- LangGraph context budget FastAPI MCP researcher LangGraph context budget observability Redis synthesizer.
- Context gateway Redis agent pipeline trace RBAC context budget RBAC MCP synthesizer.
- Synthesizer Kafka MCP BM25 MCP researcher FastAPI hybrid retrieval.
- Kafka MCP observability researcher Redis PGVector trace agent pipeline Redis Redis provenance observability MCP.
- Kafka agent pipeline synthesizer Redis Redis FastAPI LangGraph reranker FastAPI observability Kafka agent pipeline redaction.
- Agent pipeline trace reranker reranker provenance researcher reranker MCP context budget Kafka hybrid retrieval router.
