from fastapi import APIRouter, File, Form, UploadFile
from typing import Optional, Any
from app.services.chunker import parse_and_chunk, parse_and_chunk_from_url
from app.services.embedder import embed_chunks
from app.services.vector_store import store_embeddings

router = APIRouter()

@router.post("/")
async def upload_file(
    file: Optional[Any] = File(None),
    url: Optional[str] = Form(None)
):
    all_chunks = []
    namespaces = []

    # ✅ Detect actual file (not blank string from Swagger)
    if isinstance(file, UploadFile) and file.filename and file.content_type != "application/octet-stream":
        content = await file.read()
        if content:
            chunks = parse_and_chunk(content, file.filename)
            embeddings = embed_chunks(chunks)
            store_embeddings(embeddings, chunks, namespace=file.filename)
            all_chunks.append(len(chunks))
            namespaces.append(file.filename)

    # ✅ Handle URL input
    if url and url.strip():
        chunks = parse_and_chunk_from_url(url)
        domain = url.replace("https://", "").replace("http://", "").split("/")[0]
        embeddings = embed_chunks(chunks)
        store_embeddings(embeddings, chunks, namespace=domain)
        all_chunks.append(len(chunks))
        namespaces.append(domain)

    if not all_chunks:
        return {"error": "Please provide either a valid file or a valid URL."}

    return {
        "status": "success",
        "chunks": all_chunks,
        "namespaces": namespaces
    }
