from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer(os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks).tolist()
