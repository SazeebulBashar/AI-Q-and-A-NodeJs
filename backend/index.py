#Import libraries
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")


pdf_path = Path(__file__).parent / "nodejs.pdf"

# Step 1: Load the PDF document
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()


# Step 2: Split the document into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)


# Step 3: Embed the chunks and store them in a vector database (e.g., Qdrant)
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)


vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,
    url=QDRANT_URL,
    collection_name="learning-RAG"
)
