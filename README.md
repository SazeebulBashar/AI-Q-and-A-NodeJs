# Q & A - Node.js

> **Node.js Guru** — A Retrieval-Augmented Generation chatbot that answers questions about Node.js using AI.

RAGNode ingests a Node.js PDF document, indexes its content into a vector database, and lets you ask natural-language questions. Every answer is grounded in the retrieved context, reducing hallucination and keeping responses relevant to Node.js.

---

## Features

- **RAG-powered Q&A** — Uses OpenAI embeddings + Qdrant vector search to retrieve relevant document chunks before generating an answer.
- **Context-grounded responses** — The LLM only answers from the provided context, with a strict Node.js-only system prompt.
- **Chat UI** — Clean, dark-themed React interface with streaming-style interactions.
- **Fully containerized** — One `docker-compose up` runs Qdrant, the backend, and the frontend.
- **Hot-reload dev mode** — Vite dev server with API proxy for rapid frontend iteration.

---

## Architecture

```
┌──────────┐     POST /chat { query }     ┌──────────┐
│ Frontend │ ──────────────────────────►  │ Backend  │
│  React   │                              │  FastAPI │
│  Nginx   │ ◄──────────────────────────  │  Uvicorn │
└──────────┘       200 { response }       └────┬─────┘
                                               │
                                    ┌──────────┴──────────┐
                                    ▼                      ▼
                              OpenAI API              Qdrant
                          (gpt-5-nano +          (Vector DB,
                         text-embedding-3-large)   learning-RAG)
```

**Query flow:**
1. User types a question in the chat UI.
2. The frontend sends `POST /chat` with `{ "query": "..." }`.
3. The backend embeds the query, searches Qdrant for similar chunks, and builds a context.
4. OpenAI's LLM generates an answer using the retrieved context.
5. The response is returned to the UI.

---

## Tech Stack

| Layer        | Technology                                          |
| ------------ | --------------------------------------------------- |
| **Frontend** | React 19, Vite 8, Nginx                             |
| **Backend**  | Python 3.12, FastAPI, Uvicorn, LangChain, OpenAI    |
| **Vector DB**| Qdrant                                              |
| **AI**       | OpenAI `gpt-5-nano`, `text-embedding-3-large`       |
| **Infra**    | Docker, Docker Compose                              |

---

## Quick Start

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API key](https://platform.openai.com/api-keys)

### Setup

1. **Add your OpenAI API key:**

   ```bash
   echo "OPENAI_API_KEY=sk-your-key-here" > backend/.env
   ```

2. **Start all services:**

   ```bash
   docker-compose up --build
   ```

3. **Open the app:** [http://localhost](http://localhost)

The backend startup script (`start.sh`) waits for Qdrant, indexes the PDF if needed, then launches the API.

---

## Local Development

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Ensure Qdrant is running (e.g. `docker run -p 6333:6333 qdrant/qdrant`).

```bash
python index.py          # One-time: index nodejs.pdf into Qdrant
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev     # Starts Vite on :5173, proxies /chat to :8000
```

Open [http://localhost:5173](http://localhost:5173).

---

## Project Structure

```
RAGNode/
├── docker-compose.yml          # Root orchestration
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── chat.py                 # RAG pipeline (retrieve + generate)
│   ├── index.py                # PDF ingestion & embedding
│   ├── nodejs.pdf              # Source document
│   ├── requirements.txt
│   ├── Dockerfile
│   └── start.sh                # Container entrypoint
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Chat UI component
│   │   ├── App.css             # UI styles
│   │   ├── main.jsx            # React root
│   │   └── index.css           # Global styles
│   ├── Dockerfile              # Multi-stage build (Nginx)
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
```

---

## API Reference

### `POST /chat`

Send a query and receive a generated answer.

**Request:**

```json
{
  "query": "What is Node.js?"
}
```

**Response:**

```json
{
  "response": "Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine..."
}
```

**cURL example:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Node.js?"}'
```

---

## License

MIT
"# AI-Q-and-A-NodeJs" 
