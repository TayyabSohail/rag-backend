from fastapi import APIRouter, File, Form, UploadFile
from typing import Optional
from urllib.parse import urlparse
from app.services.chunker import parse_and_chunk, parse_and_chunk_from_url
from app.services.embedder import embed_chunks
from app.services.vector_store import store_embeddings
import re

router = APIRouter()

def sanitize_namespace(ns: str) -> str:
    ns = re.sub(r"[^\w\.-]", "_", ns)
    return ns.strip("._-")

@router.post("/")
async def upload_file(
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    user_id: str = Form(...)
):
    all_chunks = []
    namespaces = []

    is_valid_file = (
        file is not None
        and hasattr(file, "filename")
        and file.filename not in [None, ""]
        and file.content_type not in ["", "application/octet-stream"]
    )

    if is_valid_file:
        content = await file.read()
        if content:
            chunks = parse_and_chunk(content, file.filename)
            chunks = [c for c in chunks if c.strip()]
            if chunks:
                raw_namespace = f"{user_id}__{file.filename}"
                namespace = sanitize_namespace(raw_namespace)
                embeddings = embed_chunks(chunks)
                store_embeddings(embeddings, chunks, namespace=namespace)
                all_chunks.append(len(chunks))
                namespaces.append(namespace)

    if url and url.strip():
        domain = urlparse(url).netloc.replace("www.", "")
        chunks = parse_and_chunk_from_url(url)
        chunks = [c for c in chunks if c.strip()]
        if chunks:
            raw_namespace = f"{user_id}__{domain}"
            namespace = sanitize_namespace(raw_namespace)
            embeddings = embed_chunks(chunks)
            store_embeddings(embeddings, chunks, namespace=namespace)
            all_chunks.append(len(chunks))
            namespaces.append(namespace)

    if not all_chunks:
        return {"error": "No valid content found in file or URL."}

    return {
        "status": "success",
        "chunks": all_chunks,
        "namespaces": namespaces
    }
