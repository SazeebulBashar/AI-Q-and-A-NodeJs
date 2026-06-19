# ─── Imports ───────────────────────────────────────────────────────────────
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

# ─── Load environment variables from .env file ────────────────────────────
load_dotenv()

# ─── Initialize OpenAI client ─────────────────────────────────────────────
client = OpenAI()

# ─── Create embeddings model using OpenAI text-embedding-3-large ──────────
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
)

# ─── Connect to existing Qdrant vector database collection ────────────────
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

vector_db = QdrantVectorStore.from_existing_collection(
    url=QDRANT_URL,
    collection_name="learning-RAG",
    embedding=embeddings,
)

def get_answer(user_query: str) -> str:
    # ─── Retrieve relevant chunks from vector DB via similarity search ────────
    search_result = vector_db.similarity_search(query=user_query)

    # ─── Format retrieved chunks into a readable context string ───────────────
    context = "\n\n".join(
        f"📄 Page {int(result.metadata.get('page', 0)) + 1} | 📁 {result.metadata.get('source', 'Unknown')}\n"
        f"{'─' * 60}\n"
        f"{result.page_content}"
        for result in search_result
    )

    # ─── Build system prompt with context embedded ────────────────────────────
    system_prompt = f"""
Rules:
- Strictly follow the rules mentioned below while answering the user's question:
- Always answer based on the provided context.
- If the answer is not in the context, Just say "I only answers questions on NodeJS". Nothing else.
- Your answer should be samll and concise.

You are a helpful assistant that answers questions based on the available 
context along with the page numbers retrieved from the vector database. Use the following 
context to answer the question. Also navigate the user to open the right page in the PDF document to know more about the topic. If you don't know the answer, say you don't know. Always tryto be helpful and provide accurate information.

{context}"""

    # ─── Send prompt to LLM (GPT-5-Nano) and return the response ──────────────
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
    )

    return response.choices[0].message.content

# ─── CLI entry point ──────────────────────────────────────────────────────
if __name__ == "__main__":
    user_query = input("Hey! Tell me whats you want to know about Node JS?\n👉 ")
    answer = get_answer(user_query)
    print(f"🤖: {answer}")
