from fastapi import APIRouter, UploadFile, File
from app.services.chunker import parse_and_chunk
from app.services.embedder import embed_chunks
from app.services.vector_store import store_embeddings

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    chunks = parse_and_chunk(await file.read(), file.filename)
    embeddings = embed_chunks(chunks)
    store_embeddings(embeddings, chunks, namespace=file.filename)
    return {"status": "success", "chunks": len(chunks)}
