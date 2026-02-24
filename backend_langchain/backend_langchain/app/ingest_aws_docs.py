"""
Run this script once (or whenever docs change) to load your internal
documentation into ChromaDB.

Usage:
    docker exec -it cloud-agent-backend python -m app.ingest_aws_docs

Add any .md, .txt files to the ./docs/ folder and re-run.
"""

import os
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

DOCS_DIR = os.getenv("DOCS_DIR", "./docs")
CHROMA_HOST = "chroma"
CHROMA_PORT = 8000

def ingest():
    print(f"Loading docs from: {DOCS_DIR}")

    if not os.path.exists(DOCS_DIR):
        print(f"No docs directory found at {DOCS_DIR}. Creating it...")
        os.makedirs(DOCS_DIR)
        print("Add your .md or .txt runbooks/docs to ./docs/ and re-run.")
        return

    loader = DirectoryLoader(DOCS_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    if not documents:
        print("No documents found. Add .md files to ./docs/")
        return

    print(f"Loaded {len(documents)} documents. Splitting into chunks...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    embedding_fn = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

    vectorstore = Chroma(
        client=chroma_client,
        collection_name="aws_docs",
        embedding_function=embedding_fn,
    )

    vectorstore.add_documents(chunks)
    print(f"✅ Done. {len(chunks)} chunks ingested into ChromaDB collection 'aws_docs'.")

if __name__ == "__main__":
    ingest()
