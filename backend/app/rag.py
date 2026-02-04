import chromadb

# Create ONE client (Chroma v2 – correct way)
client = chromadb.HttpClient(
    host="chroma",
    port=8000
)

# Get existing collection
collection = client.get_or_create_collection("aws_docs")

def rag_search(query: str, n_results: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    # Chroma returns: {"documents": [[doc1, doc2, ...]]}
    return results["documents"][0]
