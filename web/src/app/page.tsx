"use client";

import { useMemo, useState } from "react";

import {
  buildIndex,
  chunkDocument,
  createRun,
  embedDocument,
  getRunSummary,
  listChunks,
  listDocuments,
  loadSampleDocuments,
  retrieve,
  uploadDocuments
} from "@/lib/api";
import type { ChunkResponse, DocumentInfo, EmbedResponse, IndexResponse, RetrieveResponse, RunSummaryResponse } from "@/lib/types";

type StepKey = "run" | "docs" | "chunk" | "embed" | "index" | "retrieve";

const STEPS: Array<{ key: StepKey; title: string; hint: string }> = [
  { key: "run", title: "1) Run", hint: "Create an isolated playground run (server-side state)." },
  { key: "docs", title: "2) Documents", hint: "Load samples or upload .txt/.md files." },
  { key: "chunk", title: "3) Chunk", hint: "Window chunking with overlap (per selected doc)." },
  { key: "embed", title: "4) Embed", hint: "Deterministic fake 384-d embeddings + previews." },
  { key: "index", title: "5) Index", hint: "Build the in-memory cosine index for this run." },
  {
    key: "retrieve",
    title: "6) Retrieve",
    hint: "Compare retrieval after rebuilding the pipeline with overlap=0 vs overlap>0."
  }
];

function formatJson(value: unknown): string {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return String(value);
  }
}

function pill(ok: boolean, label: string) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ring-1",
        ok ? "bg-emerald-500/10 text-emerald-200 ring-emerald-500/30" : "bg-slate-500/10 text-slate-200 ring-slate-500/30"
      ].join(" ")}
    >
      {label}: {ok ? "yes" : "no"}
    </span>
  );
}

export default function HomePage() {
  const [activeStep, setActiveStep] = useState<StepKey>("run");

  const [runId, setRunId] = useState<string>("");
  const [summary, setSummary] = useState<RunSummaryResponse | null>(null);

  const [docs, setDocs] = useState<DocumentInfo[]>([]);
  const [selectedDocId, setSelectedDocId] = useState<string>("");

  const [chunkSize, setChunkSize] = useState<number>(220);
  const [overlap, setOverlap] = useState<number>(40);

  const [chunks, setChunks] = useState<ChunkResponse | null>(null);
  const [embed, setEmbed] = useState<EmbedResponse | null>(null);
  const [index, setIndex] = useState<IndexResponse | null>(null);

  const [query, setQuery] = useState<string>("hybrid retrieval reranking");
  const [topK, setTopK] = useState<number>(5);

  const [resNoOverlap, setResNoOverlap] = useState<RetrieveResponse | null>(null);
  const [resWithOverlap, setResWithOverlap] = useState<RetrieveResponse | null>(null);

  const [busy, setBusy] = useState<string>("");
  const [error, setError] = useState<string>("");

  const apiBase = useMemo(() => process.env.NEXT_PUBLIC_API_BASE_URL?.trim() || "http://127.0.0.1:8000", []);

  async function refreshSummary(id: string) {
    const s = await getRunSummary(id);
    setSummary(s);
  }

  async function refreshDocuments(id: string) {
    const listed = await listDocuments(id);
    setDocs(listed.documents);
    if (!selectedDocId && listed.documents[0]) setSelectedDocId(listed.documents[0].doc_id);
    if (selectedDocId && !listed.documents.some((d) => d.doc_id === selectedDocId) && listed.documents[0]) {
      setSelectedDocId(listed.documents[0].doc_id);
    }
  }

  async function refreshChunks(id: string, docId: string) {
    if (!docId) {
      setChunks(null);
      return;
    }
    const c = await listChunks(id, docId);
    setChunks(c);
  }

  async function handleCreateRun() {
    setError("");
    setBusy("Creating run…");
    try {
      const created = await createRun();
      setRunId(created.run_id);
      setSummary(null);
      setDocs([]);
      setSelectedDocId("");
      setChunks(null);
      setEmbed(null);
      setIndex(null);
      setResNoOverlap(null);
      setResWithOverlap(null);
      await refreshSummary(created.run_id);
      setActiveStep("docs");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function handleLoadSample() {
    if (!runId) return;
    setError("");
    setBusy("Loading sample documents…");
    try {
      await loadSampleDocuments(runId);
      await refreshSummary(runId);
      await refreshDocuments(runId);
      setChunks(null);
      setEmbed(null);
      setIndex(null);
      setResNoOverlap(null);
      setResWithOverlap(null);
      setActiveStep("chunk");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function handleUpload(files: FileList | null) {
    if (!runId || !files || files.length === 0) return;
    setError("");
    setBusy("Uploading…");
    try {
      await uploadDocuments(runId, files);
      await refreshSummary(runId);
      await refreshDocuments(runId);
      setChunks(null);
      setEmbed(null);
      setIndex(null);
      setResNoOverlap(null);
      setResWithOverlap(null);
      setActiveStep("chunk");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function handleChunk() {
    if (!runId || !selectedDocId) return;
    setError("");
    setBusy("Chunking…");
    try {
      const resp = await chunkDocument(runId, { doc_id: selectedDocId, chunk_size: chunkSize, overlap });
      setChunks(resp);
      setEmbed(null);
      setIndex(null);
      setResNoOverlap(null);
      setResWithOverlap(null);
      await refreshSummary(runId);
      setActiveStep("embed");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function handleEmbed() {
    if (!runId || !selectedDocId) return;
    setError("");
    setBusy("Embedding…");
    try {
      const resp = await embedDocument(runId, selectedDocId);
      setEmbed(resp);
      setIndex(null);
      setResNoOverlap(null);
      setResWithOverlap(null);
      await refreshSummary(runId);
      setActiveStep("index");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function handleIndex() {
    if (!runId) return;
    setError("");
    setBusy("Indexing…");
    try {
      const resp = await buildIndex(runId);
      setIndex(resp);
      setResNoOverlap(null);
      setResWithOverlap(null);
      await refreshSummary(runId);
      setActiveStep("retrieve");
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setBusy("");
    }
  }

  async function pipelineThenRetrieve(overlapValue: number): Promise<RetrieveResponse> {
    if (!runId || !selectedDocId) {
      throw new Error("Missing runId or selectedDocId");
    }
    setError("");
    setBusy(`Pipeline (overlap=${overlapValue}) + retrieve…`);
    try {
      await chunkDocument(runId, { doc_id: selectedDocId, chunk_size: chunkSize, overlap: overlapValue });
      await embedDocument(runId, selectedDocId);
      await buildIndex(runId);
      const r = await retrieve(runId, { query, top_k: topK });
      await refreshSummary(runId);
      await refreshChunks(runId, selectedDocId);
      return r;
    } finally {
      setBusy("");
    }
  }

  async function handleCompareRetrieve() {
    setError("");
    setResNoOverlap(null);
    setResWithOverlap(null);
    try {
      const r0 = await pipelineThenRetrieve(0);
      setResNoOverlap(r0);
      const r1 = await pipelineThenRetrieve(Math.max(0, overlap));
      setResWithOverlap(r1);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    }
  }

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col gap-6 px-5 py-10">
      <header className="flex flex-col gap-2">
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="text-2xl font-semibold tracking-tight">RAG pipeline playground</h1>
            <p className="mt-1 max-w-3xl text-sm text-slate-300">
              This UI drives the real FastAPI playground endpoints in <span className="font-mono">/playground/*</span>. Task 5
              focuses on an explicit stepper so you can see intermediate artifacts (chunks, embedding previews, index mapping,
              retrieval).
            </p>
          </div>
          <div className="text-right text-xs text-slate-400">
            <div>
              API base: <span className="font-mono text-slate-200">{apiBase}</span>
            </div>
            <div className="mt-1">Set via NEXT_PUBLIC_API_BASE_URL</div>
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {STEPS.map((s) => {
            const active = s.key === activeStep;
            return (
              <button
                key={s.key}
                type="button"
                onClick={() => setActiveStep(s.key)}
                className={[
                  "rounded-lg px-3 py-1.5 text-sm ring-1 transition",
                  active ? "bg-indigo-500/15 text-indigo-100 ring-indigo-500/40" : "bg-slate-900 text-slate-200 ring-slate-800 hover:bg-slate-900/60"
                ].join(" ")}
              >
                {s.title}
              </button>
            );
          })}
        </div>
      </header>

      {(busy || error) && (
        <section className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
          {busy ? <div className="text-sm text-slate-200">{busy}</div> : null}
          {error ? (
            <pre className="mt-3 overflow-auto whitespace-pre-wrap rounded-lg bg-black/40 p-3 text-xs text-rose-200 ring-1 ring-rose-500/30">
              {error}
            </pre>
          ) : null}
        </section>
      )}

      <section className="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <div className="lg:col-span-7">
          {activeStep === "run" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Create run</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "run")?.hint}</p>
              <div className="mt-4 flex flex-wrap items-center gap-3">
                <button
                  type="button"
                  onClick={handleCreateRun}
                  className="rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
                  disabled={!!busy}
                >
                  Create new run
                </button>
                {runId ? (
                  <div className="text-sm text-slate-200">
                    Active run: <span className="font-mono">{runId}</span>
                  </div>
                ) : (
                  <div className="text-sm text-slate-400">No active run yet.</div>
                )}
              </div>
            </div>
          )}

          {activeStep === "docs" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Documents</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "docs")?.hint}</p>

              {!runId ? (
                <p className="mt-4 text-sm text-slate-400">Create a run first.</p>
              ) : (
                <div className="mt-4 flex flex-col gap-4">
                  <div className="flex flex-wrap gap-3">
                    <button
                      type="button"
                      onClick={handleLoadSample}
                      className="rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-950 hover:bg-white disabled:opacity-50"
                      disabled={!!busy}
                    >
                      Load sample corpus
                    </button>
                    <label className="inline-flex cursor-pointer items-center gap-2 rounded-lg bg-slate-950 px-4 py-2 text-sm font-medium text-slate-100 ring-1 ring-slate-800 hover:bg-slate-950/60">
                      <input
                        type="file"
                        multiple
                        accept=".txt,.md,text/plain,text/markdown"
                        className="hidden"
                        disabled={!!busy}
                        onChange={(e) => void handleUpload(e.target.files)}
                      />
                      Upload .txt / .md
                    </label>
                  </div>

                  <div>
                    <div className="text-xs font-medium text-slate-400">Loaded documents</div>
                    <div className="mt-2 overflow-hidden rounded-lg border border-slate-800">
                      <table className="w-full border-collapse text-sm">
                        <thead className="bg-slate-950/60 text-left text-xs text-slate-400">
                          <tr>
                            <th className="px-3 py-2">Select</th>
                            <th className="px-3 py-2">Name</th>
                            <th className="px-3 py-2">Type</th>
                            <th className="px-3 py-2 text-right">Chars</th>
                          </tr>
                        </thead>
                        <tbody>
                          {docs.length === 0 ? (
                            <tr>
                              <td className="px-3 py-3 text-slate-400" colSpan={4}>
                                No documents yet.
                              </td>
                            </tr>
                          ) : (
                            docs.map((d) => {
                              const checked = d.doc_id === selectedDocId;
                              return (
                                <tr key={d.doc_id} className="border-t border-slate-800">
                                  <td className="px-3 py-2">
                                    <input
                                      type="radio"
                                      name="doc"
                                      checked={checked}
                                      onChange={() => {
                                        setSelectedDocId(d.doc_id);
                                        void (async () => {
                                          try {
                                            await refreshChunks(runId, d.doc_id);
                                          } catch (e) {
                                            setError(e instanceof Error ? e.message : String(e));
                                          }
                                        })();
                                      }}
                                    />
                                  </td>
                                  <td className="px-3 py-2 font-mono text-xs text-slate-200">{d.name}</td>
                                  <td className="px-3 py-2 text-xs text-slate-300">{d.content_type}</td>
                                  <td className="px-3 py-2 text-right text-xs text-slate-300">{d.size_chars}</td>
                                </tr>
                              );
                            })
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeStep === "chunk" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Chunking</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "chunk")?.hint}</p>

              {!runId ? (
                <p className="mt-4 text-sm text-slate-400">Create a run first.</p>
              ) : !selectedDocId ? (
                <p className="mt-4 text-sm text-slate-400">Load documents and select a doc.</p>
              ) : (
                <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">
                  <label className="flex flex-col gap-1 text-sm">
                    <span className="text-xs font-medium text-slate-400">Chunk size (chars)</span>
                    <input
                      className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 font-mono text-sm outline-none ring-0 focus:border-indigo-500/60"
                      inputMode="numeric"
                      value={String(chunkSize)}
                      onChange={(e) => setChunkSize(Number(e.target.value || 0))}
                    />
                  </label>
                  <label className="flex flex-col gap-1 text-sm">
                    <span className="text-xs font-medium text-slate-400">Overlap (chars)</span>
                    <input
                      className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 font-mono text-sm outline-none ring-0 focus:border-indigo-500/60"
                      inputMode="numeric"
                      value={String(overlap)}
                      onChange={(e) => setOverlap(Number(e.target.value || 0))}
                    />
                  </label>
                  <div className="flex items-end">
                    <button
                      type="button"
                      onClick={handleChunk}
                      className="w-full rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
                      disabled={!!busy}
                    >
                      Run chunking
                    </button>
                  </div>

                  <div className="md:col-span-3">
                    <div className="text-xs font-medium text-slate-400">Chunk previews</div>
                    <div className="mt-2 max-h-[420px] overflow-auto rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                      {!chunks || chunks.chunks.length === 0 ? (
                        <div className="text-sm text-slate-400">No chunks loaded for this doc yet.</div>
                      ) : (
                        <ol className="space-y-3">
                          {chunks.chunks.map((c) => (
                            <li key={c.chunk_id} className="rounded-lg bg-black/25 p-3 ring-1 ring-slate-800">
                              <div className="flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400">
                                <div className="font-mono text-slate-200">{c.chunk_id}</div>
                                <div className="font-mono">
                                  [{c.start_char}, {c.end_char})
                                </div>
                              </div>
                              <div className="mt-2 text-sm text-slate-100">{c.text_preview}</div>
                            </li>
                          ))}
                        </ol>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeStep === "embed" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Embeddings</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "embed")?.hint}</p>

              {!runId || !selectedDocId ? (
                <p className="mt-4 text-sm text-slate-400">Select a document and chunk it first.</p>
              ) : (
                <div className="mt-4 flex flex-col gap-4">
                  <button
                    type="button"
                    onClick={handleEmbed}
                    className="w-fit rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
                    disabled={!!busy}
                  >
                    Embed chunks for selected doc
                  </button>

                  {!embed ? (
                    <div className="text-sm text-slate-400">No embedding response loaded yet.</div>
                  ) : (
                    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                      <div>
                        <div className="text-xs font-medium text-slate-400">Mapping preview</div>
                        <pre className="mt-2 max-h-[320px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                          {formatJson(embed.mapping_preview)}
                        </pre>
                      </div>
                      <div>
                        <div className="text-xs font-medium text-slate-400">Vector preview (first dims)</div>
                        <pre className="mt-2 max-h-[320px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                          {formatJson({ dim: embed.dim, vectors_preview: embed.vectors_preview })}
                        </pre>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeStep === "index" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Index</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "index")?.hint}</p>

              {!runId ? (
                <p className="mt-4 text-sm text-slate-400">Create a run first.</p>
              ) : (
                <div className="mt-4 flex flex-col gap-4">
                  <button
                    type="button"
                    onClick={handleIndex}
                    className="w-fit rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
                    disabled={!!busy}
                  >
                    Build index (all embedded docs in this run)
                  </button>

                  {!index ? (
                    <div className="text-sm text-slate-400">No index response loaded yet.</div>
                  ) : (
                    <div>
                      <div className="text-xs font-medium text-slate-400">Index stats + mapping preview</div>
                      <pre className="mt-2 max-h-[360px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                        {formatJson({ indexed: index.indexed, mapping_preview: index.mapping_preview })}
                      </pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {activeStep === "retrieve" && (
            <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-semibold">Retrieve + overlap comparison</h2>
              <p className="mt-2 text-sm text-slate-300">{STEPS.find((s) => s.key === "retrieve")?.hint}</p>

              {!runId || !selectedDocId ? (
                <p className="mt-4 text-sm text-slate-400">Select a document first.</p>
              ) : (
                <div className="mt-4 flex flex-col gap-4">
                  <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                    <label className="md:col-span-2 flex flex-col gap-1 text-sm">
                      <span className="text-xs font-medium text-slate-400">Query</span>
                      <input
                        className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-indigo-500/60"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                      />
                    </label>
                    <label className="flex flex-col gap-1 text-sm">
                      <span className="text-xs font-medium text-slate-400">top_k</span>
                      <input
                        className="rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 font-mono text-sm outline-none focus:border-indigo-500/60"
                        inputMode="numeric"
                        value={String(topK)}
                        onChange={(e) => setTopK(Number(e.target.value || 0))}
                      />
                    </label>
                  </div>

                  <div className="rounded-lg border border-slate-800 bg-slate-950/40 p-3 text-sm text-slate-200">
                    <div className="text-xs font-medium text-slate-400">What “compare” does</div>
                    <div className="mt-2 text-sm text-slate-300">
                      This runs an end-to-end refresh for the <span className="font-mono">selected doc only</span>: chunk → embed →
                      index → retrieve. It does it twice: first with <span className="font-mono">overlap=0</span>, then with{" "}
                      <span className="font-mono">overlap={Math.max(0, overlap)}</span> (from the Chunk step controls).
                    </div>
                  </div>

                  <button
                    type="button"
                    onClick={handleCompareRetrieve}
                    className="w-fit rounded-lg bg-indigo-500 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-400 disabled:opacity-50"
                    disabled={!!busy}
                  >
                    Run side-by-side comparison
                  </button>

                  <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                    <div>
                      <div className="text-xs font-medium text-slate-400">A) overlap = 0</div>
                      {!resNoOverlap ? (
                        <div className="mt-2 text-sm text-slate-400">No results yet.</div>
                      ) : (
                        <pre className="mt-2 max-h-[520px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                          {formatJson(resNoOverlap)}
                        </pre>
                      )}
                    </div>
                    <div>
                      <div className="text-xs font-medium text-slate-400">B) overlap = {Math.max(0, overlap)}</div>
                      {!resWithOverlap ? (
                        <div className="mt-2 text-sm text-slate-400">No results yet.</div>
                      ) : (
                        <pre className="mt-2 max-h-[520px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                          {formatJson(resWithOverlap)}
                        </pre>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <aside className="lg:col-span-5">
          <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5">
            <h2 className="text-lg font-semibold">Run state</h2>
            <p className="mt-2 text-sm text-slate-300">
              Summary from <span className="font-mono">GET /playground/runs/{"{run_id}"}</span>.
            </p>

            <div className="mt-4 flex flex-wrap gap-2">
              <button
                type="button"
                className="rounded-lg bg-slate-950 px-3 py-1.5 text-xs font-medium text-slate-100 ring-1 ring-slate-800 hover:bg-slate-950/60 disabled:opacity-50"
                disabled={!runId || !!busy}
                onClick={async () => {
                  if (!runId) return;
                  setError("");
                  setBusy("Refreshing…");
                  try {
                    await refreshSummary(runId);
                    await refreshDocuments(runId);
                    await refreshChunks(runId, selectedDocId);
                  } catch (e) {
                    setError(e instanceof Error ? e.message : String(e));
                  } finally {
                    setBusy("");
                  }
                }}
              >
                Refresh summary + docs
              </button>
            </div>

            {!summary ? (
              <p className="mt-4 text-sm text-slate-400">No summary yet.</p>
            ) : (
              <div className="mt-4 space-y-3">
                <div className="flex flex-wrap gap-2">
                  {pill(summary.has_documents, "docs")}
                  {pill(summary.has_chunks, "chunks")}
                  {pill(summary.has_embeddings, "embeds")}
                  {pill(summary.has_index, "index")}
                </div>

                <pre className="max-h-[520px] overflow-auto rounded-lg bg-black/40 p-3 text-xs text-slate-100 ring-1 ring-slate-800">
                  {formatJson(summary)}
                </pre>
              </div>
            )}
          </div>

          <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/30 p-5">
            <h2 className="text-lg font-semibold">Quick tips</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-slate-300">
              <li>
                Start the API from the repo root: <span className="font-mono">uvicorn app.main:app --reload --port 8000</span>
              </li>
              <li>
                Start the UI from <span className="font-mono">web/</span>: <span className="font-mono">npm install</span> then{" "}
                <span className="font-mono">npm run dev</span>
              </li>
              <li>
                If the browser blocks requests, confirm CORS settings in <span className="font-mono">app/core/config.py</span> /{" "}
                <span className="font-mono">.env</span>.
              </li>
            </ul>
          </div>
        </aside>
      </section>
    </main>
  );
}
