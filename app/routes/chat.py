from fastapi import APIRouter
from app.models.schemas import ChatQuery
from app.services.embedder import model
from app.services.vector_store import query_similar_chunks
from app.services.llm_client import query_llm

router = APIRouter()

def sanitize_namespace(ns: str) -> str:
    return ns.replace("https://", "").replace("http://", "").split("/")[0]

@router.post("/")
async def chat(query: ChatQuery):
    query_vec = model.encode([query.question]).tolist()[0]

    # ✅ sanitize here!
    safe_namespace = sanitize_namespace(query.namespace)

    chunks = query_similar_chunks(query_vec, namespace=safe_namespace)
    context = "\n".join(chunks)

    prompt = f"Answer based on the context:\n\n{context}\n\nQuestion: {query.question}"
    answer = await query_llm(prompt)

    return {"answer": answer}
