import type {
  ChunkResponse,
  CreateRunResponse,
  EmbedResponse,
  IndexResponse,
  ListDocumentsResponse,
  RetrieveResponse,
  RunSummaryResponse
} from "@/lib/types";

function getApiBaseUrl(): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL?.trim();
  if (!base) return "http://127.0.0.1:8000";
  return base.replace(/\/+$/, "");
}

async function readErrorMessage(res: Response): Promise<string> {
  const ct = res.headers.get("content-type") ?? "";
  try {
    if (ct.includes("application/json")) {
      const data = (await res.json()) as unknown;
      if (data && typeof data === "object" && "detail" in data) {
        const detail = (data as { detail?: unknown }).detail;
        if (typeof detail === "string") return detail;
        return JSON.stringify(detail);
      }
      return JSON.stringify(data);
    }
    return await res.text();
  } catch {
    return res.statusText;
  }
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${getApiBaseUrl()}${path}`;
  const res = await fetch(url, {
    ...init,
    headers: {
      Accept: "application/json",
      ...(init?.headers ?? {})
    }
  });

  if (!res.ok) {
    const msg = await readErrorMessage(res);
    throw new ApiError(res.status, msg || `HTTP ${res.status}`);
  }

  return (await res.json()) as T;
}

export async function createRun(): Promise<CreateRunResponse> {
  return await apiFetch<CreateRunResponse>("/playground/runs", { method: "POST" });
}

export async function getRunSummary(runId: string): Promise<RunSummaryResponse> {
  return await apiFetch<RunSummaryResponse>(`/playground/runs/${encodeURIComponent(runId)}`);
}

export async function loadSampleDocuments(runId: string): Promise<{ loaded: number }> {
  return await apiFetch<{ loaded: number }>(
    `/playground/runs/${encodeURIComponent(runId)}/documents:load-sample`,
    { method: "POST" }
  );
}

export async function uploadDocuments(runId: string, files: FileList | File[]): Promise<{ uploaded: number }> {
  const fd = new FormData();
  for (const f of Array.from(files)) fd.append("files", f);

  const url = `${getApiBaseUrl()}/playground/runs/${encodeURIComponent(runId)}/documents:upload`;
  const res = await fetch(url, { method: "POST", body: fd });
  if (!res.ok) throw new ApiError(res.status, await readErrorMessage(res));
  return (await res.json()) as { uploaded: number };
}

export async function listDocuments(runId: string): Promise<ListDocumentsResponse> {
  return await apiFetch<ListDocumentsResponse>(`/playground/runs/${encodeURIComponent(runId)}/documents`);
}

export async function chunkDocument(
  runId: string,
  body: {
    doc_id: string;
    chunk_size: number;
    overlap: number;
    strategy?: "structured" | "window";
    max_chunk_chars?: number | null;
  }
): Promise<ChunkResponse> {
  return await apiFetch<ChunkResponse>(`/playground/runs/${encodeURIComponent(runId)}/chunk`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
}

export async function listChunks(runId: string, docId: string): Promise<ChunkResponse> {
  const q = new URLSearchParams({ doc_id: docId });
  return await apiFetch<ChunkResponse>(`/playground/runs/${encodeURIComponent(runId)}/chunks?${q.toString()}`);
}

export async function embedDocument(runId: string, docId: string): Promise<EmbedResponse> {
  return await apiFetch<EmbedResponse>(`/playground/runs/${encodeURIComponent(runId)}/embed`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doc_id: docId })
  });
}

export async function buildIndex(runId: string): Promise<IndexResponse> {
  return await apiFetch<IndexResponse>(`/playground/runs/${encodeURIComponent(runId)}/index`, { method: "POST" });
}

export async function retrieve(runId: string, body: { query: string; top_k: number }): Promise<RetrieveResponse> {
  return await apiFetch<RetrieveResponse>(`/playground/runs/${encodeURIComponent(runId)}/retrieve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
}
