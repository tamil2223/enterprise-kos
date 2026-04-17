# Incident Postmortem: Cold-start performance (ZenithLogistics)

**Doc ID:** doc_8642_eypmre38
**Company:** ZenithLogistics
**Owner:** dave (Infra)
**Created:** 2026-04-15

            ## Summary

            SEV-2 incident `INC-9907` impacted responses produced by the agent pipeline (Router → Researcher → Synthesizer).
            Users observed inconsistent citations and context truncation under load.

            ## Impact

            - Synthesizer agent pipeline MCP context budget Kafka BM25 Kafka FastAPI FastAPI.
- Provenance trace agent pipeline LangGraph hybrid retrieval context budget Kafka researcher BM25 Redis RBAC.
- Kafka trace observability FastAPI hybrid retrieval context gateway trace MCP PGVector context budget FastAPI researcher Kafka.
- Context gateway FastAPI synthesizer reranker reranker redaction RBAC synthesizer hybrid retrieval BM25.
- FastAPI reranker provenance synthesizer researcher synthesizer provenance context gateway researcher RBAC Kafka reranker.

            ## Root Cause

            PGVector RBAC synthesizer trace context gateway reranker FastAPI router MCP LangGraph redaction context budget. Reranker reranker context gateway FastAPI agent pipeline researcher hybrid retrieval hybrid retrieval trace context gateway reranker router. Router PGVector BM25 observability agent pipeline redaction provenance provenance. Observability agent pipeline hybrid retrieval agent pipeline context budget BM25 Redis context budget synthesizer trace redaction. Redaction PGVector FastAPI MCP BM25 PGVector RBAC provenance agent pipeline.

            ## Detection

            Reranker provenance router RBAC context budget FastAPI LangGraph researcher PGVector BM25 reranker LangGraph. Hybrid retrieval hybrid retrieval FastAPI Redis researcher observability LangGraph redaction. Redaction observability agent pipeline router researcher BM25 FastAPI PGVector context budget Redis context budget RBAC PGVector.

            ## Resolution

            - Reranker MCP LangGraph researcher RBAC hybrid retrieval Kafka hybrid retrieval context gateway Kafka LangGraph.
- Trace context budget context budget provenance Redis synthesizer trace MCP researcher trace Kafka context gateway provenance.
- Kafka agent pipeline agent pipeline provenance hybrid retrieval Redis redaction observability.
- RBAC PGVector hybrid retrieval FastAPI Redis context budget synthesizer Kafka PGVector router provenance RBAC PGVector Redis.
- PGVector Redis redaction provenance synthesizer hybrid retrieval Kafka LangGraph RBAC router FastAPI provenance reranker.
- FastAPI LangGraph observability MCP Kafka provenance MCP trace.

            ## Follow-ups

            - Synthesizer reranker reranker PGVector researcher PGVector redaction provenance provenance FastAPI PGVector RBAC context budget.
- FastAPI LangGraph researcher MCP Redis Kafka LangGraph trace observability observability FastAPI BM25 MCP.
- Trace LangGraph Redis router trace trace context budget trace MCP LangGraph FastAPI router.
- Context gateway agent pipeline agent pipeline reranker Kafka reranker LangGraph reranker router Redis hybrid retrieval FastAPI redaction Redis.
- Router provenance provenance reranker LangGraph provenance context budget RBAC reranker observability MCP context budget synthesizer.
- PGVector redaction hybrid retrieval redaction hybrid retrieval BM25 researcher FastAPI context budget provenance.
- Context gateway LangGraph context budget hybrid retrieval hybrid retrieval router provenance Kafka MCP synthesizer reranker synthesizer FastAPI.
- Kafka hybrid retrieval agent pipeline Redis PGVector BM25 researcher trace redaction Kafka observability researcher observability observability.



### Appendix 0: f9b2ac7629ab-0

Kafka agent pipeline MCP context budget router hybrid retrieval synthesizer observability observability FastAPI FastAPI redaction. PGVector agent pipeline trace agent pipeline LangGraph redaction BM25 context gateway FastAPI PGVector BM25 agent pipeline redaction PGVector. PGVector context gateway reranker Redis reranker researcher router reranker redaction RBAC router agent pipeline MCP hybrid retrieval. MCP Redis agent pipeline FastAPI router hybrid retrieval Kafka Kafka observability redaction RBAC observability FastAPI. Redis hybrid retrieval LangGraph hybrid retrieval observability trace Kafka LangGraph. BM25 context budget Kafka provenance provenance PGVector Redis synthesizer redaction hybrid retrieval RBAC researcher BM25.

- Router FastAPI researcher LangGraph reranker LangGraph observability FastAPI synthesizer PGVector.
- Kafka FastAPI PGVector context budget redaction PGVector context gateway Redis researcher RBAC hybrid retrieval LangGraph RBAC provenance.
- Synthesizer provenance observability hybrid retrieval reranker synthesizer PGVector Redis hybrid retrieval agent pipeline Redis hybrid retrieval redaction context gateway.
- FastAPI Redis BM25 router router researcher researcher context budget observability redaction observability context budget MCP.
- BM25 Kafka observability RBAC Kafka trace synthesizer synthesizer PGVector synthesizer router MCP.
- Provenance provenance synthesizer BM25 Kafka MCP Redis BM25.
- Hybrid retrieval context gateway Kafka Redis synthesizer MCP Kafka reranker reranker provenance Kafka hybrid retrieval agent pipeline.
- Agent pipeline PGVector trace hybrid retrieval synthesizer FastAPI trace context budget trace MCP Redis synthesizer.

### Appendix 1: f9b2ac7629ab-1

Kafka router RBAC router provenance agent pipeline trace redaction researcher agent pipeline context budget observability. BM25 researcher router researcher Redis redaction Redis redaction FastAPI BM25 provenance. Redis observability trace RBAC observability RBAC Redis provenance redaction observability. PGVector context gateway BM25 Kafka router provenance synthesizer router. Synthesizer LangGraph reranker reranker RBAC researcher synthesizer LangGraph agent pipeline synthesizer. MCP PGVector context budget trace trace redaction redaction redaction trace researcher.

- Trace PGVector FastAPI router reranker BM25 context gateway researcher redaction.
- Provenance router router Kafka context budget PGVector observability router researcher MCP context gateway FastAPI redaction.
- FastAPI observability router MCP PGVector LangGraph LangGraph FastAPI redaction agent pipeline.
- Synthesizer Redis agent pipeline redaction FastAPI hybrid retrieval LangGraph BM25 synthesizer observability LangGraph provenance observability context budget.
- Redis LangGraph hybrid retrieval Redis redaction observability BM25 RBAC observability MCP context budget.
- Synthesizer agent pipeline synthesizer Kafka context gateway context budget Redis provenance MCP.
- Reranker FastAPI MCP FastAPI PGVector Redis Redis hybrid retrieval trace agent pipeline.
- Researcher synthesizer Redis trace MCP FastAPI hybrid retrieval observability synthesizer agent pipeline researcher RBAC Redis.

### Appendix 2: f9b2ac7629ab-2

Router BM25 BM25 FastAPI Redis Redis router researcher researcher researcher RBAC. RBAC Kafka researcher hybrid retrieval Kafka LangGraph FastAPI researcher. RBAC context budget trace FastAPI synthesizer agent pipeline reranker MCP reranker BM25 PGVector. PGVector trace trace MCP Kafka hybrid retrieval FastAPI RBAC context gateway Kafka trace hybrid retrieval Redis RBAC. RBAC provenance agent pipeline router context budget FastAPI Redis context budget trace. Redis hybrid retrieval reranker router context gateway LangGraph synthesizer researcher PGVector.

- Redis redaction trace context gateway hybrid retrieval context budget PGVector FastAPI context gateway MCP.
- Trace router researcher provenance BM25 LangGraph MCP trace MCP.
- Context budget context gateway agent pipeline Kafka provenance provenance hybrid retrieval provenance researcher Kafka researcher provenance researcher.
- MCP agent pipeline router provenance FastAPI Kafka Redis Kafka context gateway.
- Context gateway synthesizer Redis trace PGVector context gateway agent pipeline observability provenance MCP.
- LangGraph synthesizer synthesizer trace RBAC Kafka agent pipeline trace hybrid retrieval Kafka provenance Kafka trace RBAC.
- Hybrid retrieval MCP researcher redaction trace Kafka Kafka synthesizer Kafka researcher reranker.
- FastAPI context budget hybrid retrieval provenance agent pipeline LangGraph provenance context gateway provenance researcher observability.

### Appendix 3: f9b2ac7629ab-3

FastAPI Kafka router reranker synthesizer MCP Redis redaction Kafka. Hybrid retrieval Kafka reranker researcher trace hybrid retrieval redaction FastAPI researcher provenance LangGraph. Context budget FastAPI PGVector reranker researcher RBAC observability router Kafka context gateway. Context gateway researcher BM25 researcher trace LangGraph context gateway LangGraph BM25 router reranker. Synthesizer redaction RBAC FastAPI Redis context budget FastAPI PGVector researcher MCP PGVector Kafka redaction. Hybrid retrieval RBAC redaction context gateway router reranker router PGVector.

- Reranker PGVector PGVector researcher PGVector Kafka FastAPI agent pipeline router Kafka context budget agent pipeline.
- MCP synthesizer Redis router researcher RBAC synthesizer hybrid retrieval provenance synthesizer BM25.
- Agent pipeline provenance trace hybrid retrieval Redis Redis Kafka trace.
- Trace BM25 researcher context budget redaction hybrid retrieval PGVector BM25 agent pipeline synthesizer.
- Provenance trace RBAC agent pipeline agent pipeline hybrid retrieval trace FastAPI context budget trace.
- Context budget RBAC Kafka FastAPI trace router BM25 context gateway.
- Synthesizer RBAC Redis trace hybrid retrieval trace Kafka redaction context budget context budget.
- Context gateway researcher MCP provenance reranker researcher LangGraph MCP reranker context budget.

### Appendix 4: f9b2ac7629ab-4

Redaction agent pipeline PGVector redaction RBAC context budget FastAPI LangGraph. LangGraph context budget FastAPI Kafka PGVector context budget reranker synthesizer synthesizer BM25 router hybrid retrieval researcher trace. PGVector LangGraph reranker redaction redaction context budget observability Kafka. Observability synthesizer Kafka FastAPI MCP LangGraph provenance RBAC MCP synthesizer context budget context budget context gateway. LangGraph Redis researcher context budget LangGraph agent pipeline context budget redaction hybrid retrieval BM25 context budget researcher PGVector. BM25 observability synthesizer BM25 hybrid retrieval trace hybrid retrieval BM25 provenance.

- Router context gateway LangGraph RBAC FastAPI agent pipeline context budget FastAPI FastAPI MCP synthesizer.
- LangGraph router Redis agent pipeline synthesizer researcher PGVector researcher hybrid retrieval LangGraph LangGraph.
- Observability Redis context budget BM25 RBAC provenance reranker researcher agent pipeline Kafka Redis.
- Provenance researcher context gateway LangGraph BM25 Kafka researcher observability Kafka provenance MCP PGVector MCP.
- Agent pipeline hybrid retrieval hybrid retrieval RBAC LangGraph redaction observability Kafka synthesizer Redis researcher Kafka PGVector redaction.
- FastAPI router context gateway MCP trace context gateway FastAPI synthesizer Redis researcher LangGraph.
- MCP LangGraph provenance provenance LangGraph trace reranker FastAPI agent pipeline observability observability Kafka observability Redis.
- LangGraph context gateway observability BM25 PGVector agent pipeline context budget provenance FastAPI.
