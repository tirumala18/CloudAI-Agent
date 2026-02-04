import requests
import sys
sys.path.append("/app")
from bs4 import BeautifulSoup
import chromadb
from app.chunk import chunk_text

client = chromadb.HttpClient(host="chroma", port=8000)
collection = client.get_or_create_collection("aws_docs")

def fetch_text(url):
    html = requests.get(url, timeout=15).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)

def ingest(url, doc_id):
    text = fetch_text(url)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[f"{doc_id}_{i}"],
            metadatas=[{"source": url}]
        )

# START SMALL (do NOT crawl everything yet)
ingest(
    "https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListBuckets.html",
    "s3_list_buckets"
)

ingest(
    "https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeInstances.html",
    "ec2_describe_instances"
)

print("AWS docs ingested")
