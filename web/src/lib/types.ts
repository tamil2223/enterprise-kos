export type CreateRunResponse = {
  run_id: string;
};

export type RunSummaryResponse = {
  run_id: string;
  documents_count: number;
  chunked_docs_count: number;
  embedded_docs_count: number;
  indexed_vectors_count: number;
  has_documents: boolean;
  has_chunks: boolean;
  has_embeddings: boolean;
  has_index: boolean;
};

export type DocumentInfo = {
  doc_id: string;
  name: string;
  content_type: string;
  size_chars: number;
};

export type ListDocumentsResponse = {
  documents: DocumentInfo[];
};

export type ChunkInfo = {
  chunk_id: string;
  doc_id: string;
  chunk_index: number;
  start_char: number;
  end_char: number;
  text_preview: string;
  embed_text_preview?: string | null;
  strategy?: string | null;
  section_id?: string | null;
  section_title?: string | null;
  heading_path?: string | null;
  source_name?: string | null;
  section_chunk_index?: number | null;
};

export type ChunkResponse = {
  doc_id: string;
  chunk_size: number;
  overlap: number;
  strategy?: string;
  max_chunk_chars?: number | null;
  chunks: ChunkInfo[];
};

export type EmbedResponse = {
  doc_id: string;
  dim: number;
  mapping_preview: Array<Record<string, string>>;
  vectors_preview: number[][];
};

export type IndexResponse = {
  indexed: number;
  mapping_preview: Array<Record<string, string>>;
};

export type RetrieveResult = {
  rank: number;
  score: number;
  doc_id: string;
  chunk_id: string;
  vector_id: string;
  chunk_preview: string;
};

export type RetrieveResponse = {
  query: string;
  top_k: number;
  query_vector_preview: number[];
  results: RetrieveResult[];
};
