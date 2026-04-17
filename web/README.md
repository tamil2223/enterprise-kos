# RAG Playground Web UI

Next.js UI for the FastAPI `/playground/*` endpoints.

## Dev

From `web/`:

```bash
npm install
npm run dev
```

Next.js will listen on **`http://127.0.0.1:3000`** (pinned in `package.json`) so it does not collide with the API on **`:8000`**.

Set the API base URL (optional; defaults to `http://127.0.0.1:8000`):

```bash
export NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000"
```

## API

Run the backend (repo root):

```bash
uvicorn app.main:app --reload --port 8000
```

If the browser reports CORS issues, update `CORS_ALLOW_ORIGINS` / `CORS_ALLOW_ORIGIN_REGEX` in `.env` (see `.env.example`).
