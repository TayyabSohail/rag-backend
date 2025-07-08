from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer(os.getenv("EMBED_MODEL", "intfloat/e5-small-v2"))

def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks).tolist()
