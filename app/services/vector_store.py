import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = os.getenv("CHROMA_PATH", "chroma_store")
client = chromadb.PersistentClient(path=CHROMA_PATH)

def store_embeddings(embeddings, chunks, namespace="default"):
    collection = client.get_or_create_collection(name=namespace)
    for i, (vec, chunk) in enumerate(zip(embeddings, chunks)):
        collection.add(
            documents=[chunk],
            embeddings=[vec],
            ids=[f"{namespace}-{i}"]
        )

def query_similar_chunks(query_embedding, namespace="default", top_k=5):
    collection = client.get_or_create_collection(name=namespace)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results['documents'][0]
