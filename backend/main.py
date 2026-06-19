from fastapi import FastAPI
from pydantic import BaseModel
from chat import get_answer
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG Chat API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost", "http://localhost:80"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str


@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    answer = get_answer(request.query)
    return QueryResponse(answer=answer)


if __name__ == "__main__":
    
    uvicorn.run(app, host="localhost", port=8000)
