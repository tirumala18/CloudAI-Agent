import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.tools import tool

# Local embeddings — no OpenAI key needed
embedding_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

import os

# Connect to running ChromaDB container
CHROMA_HOST = os.getenv("CHROMA_HOST", "chroma")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))
chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

vectorstore = Chroma(
    client=chroma_client,
    collection_name="aws_docs",
    embedding_function=embedding_fn,
)

@tool
def rag_search(query: str) -> str:
    """
    Search internal DevOps documentation, runbooks, service catalog,
    deployment guides, and architecture docs.
    Use this when asked about internal processes, service ownership,
    deployment conventions, team contacts, or anything not available via AWS APIs.
    """
    docs = vectorstore.similarity_search(query, k=4)
    if not docs:
        return "No relevant documentation found in internal knowledge base."
    return "\n\n---\n\n".join([d.page_content for d in docs])
