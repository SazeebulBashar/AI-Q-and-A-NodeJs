# Commands Reference — Node JS Guru (RAG Chatbot)

## Docker Commands

| Command | Description |
|---------|-------------|
| `docker compose up --build` | Build and start all services (Qdrant + Backend + Frontend) |
| `docker compose up -d` | Start all services in detached (background) mode |
| `docker compose down` | Stop and remove all containers |
| `docker compose down -v` | Stop and remove containers **including volumes** (wipes Qdrant data) |
| `docker compose logs -f` | Follow live logs from all services |
| `docker compose logs -f backend` | Follow logs from the backend service only |
| `docker compose ps` | List running services and their status |
| `docker compose build` | Rebuild images without starting containers |
| `docker compose exec backend python index.py` | Re-run PDF indexing inside the running backend container |
| `docker run -p 6333:6333 qdrant/qdrant` | Run Qdrant standalone (for local development) |

## Python Commands (Backend)

| Command | Description |
|---------|-------------|
| `python -m venv .venv` | Create a Python virtual environment |
| `.venv\Scripts\activate` | Activate the virtual environment (Windows) |
| `source .venv/bin/activate` | Activate the virtual environment (macOS/Linux) |
| `pip install -r requirements.txt` | Install all Python dependencies |
| `python index.py` | Index `nodejs.pdf` into Qdrant (one-time setup) |
| `uvicorn main:app --reload --port 8000` | Start the FastAPI backend with hot-reload on port 8000 |
| `uvicorn main:app --host 0.0.0.0 --port 8000` | Start the backend bound to all network interfaces |

## Node.js Commands (Frontend)

| Command | Description |
|---------|-------------|
| `npm install` | Install all frontend dependencies |
| `npm run dev` | Start the Vite dev server (port 5173, proxies `/chat` to `:8000`) |
| `npm run build` | Build the frontend for production (output to `dist/`) |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint across the frontend source code |

## API Testing

| Command | Description |
|---------|-------------|
| `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{\"query\": \"What is Node.js?\"}"` | Send a test query to the chat API |
| `curl -s http://localhost:6333/collections` | Check if Qdrant is running and list collections |

## Environment Setup

| Command | Description |
|---------|-------------|
| `echo OPENAI_API_KEY=sk-your-key-here > backend\.env` | Create the `.env` file with your OpenAI API key |

## Git Commands

| Command | Description |
|---------|-------------|
| `git status` | Show working tree status |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Commit staged changes |
| `git log --oneline -10` | View last 10 commits (compact) |
| `git diff` | View unstaged changes |
| `git push origin main` | Push commits to remote main branch |

## Useful Utilities

| Command | Description |
|---------|-------------|
| `docker ps` | List running Docker containers |
| `docker images` | List built Docker images |
| `docker system prune -a` | Remove all unused containers, images, and cache |
| `python --version` | Check Python version |
| `node --version` | Check Node.js version |
| `npm --version` | Check npm version |
