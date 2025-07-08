from fastapi import APIRouter
from app.models.schemas import ChatQuery
from app.services.embedder import model
from app.services.vector_store import query_similar_chunks
from app.services.llm_client import query_llm
import re

router = APIRouter()

def sanitize_namespace(ns: str) -> str:
    ns = re.sub(r"[^\w\.-]", "_", ns)
    return ns.strip("._-")

@router.post("/")
async def chat(query: ChatQuery):
    query_vec = model.encode([query.question]).tolist()[0]
    
    raw_namespace = f"{query.user_id}__{query.namespace}"
    full_namespace = sanitize_namespace(raw_namespace)

    chunks = query_similar_chunks(query_vec, namespace=full_namespace)
    context = "\n".join(chunks)

    system_prompt = {
        "role": "system",
        "content": "You are an assistant answering using uploaded documents."
    }
    messages = [system_prompt]

    if query.history:
        messages.extend(query.history)

    messages.append({
        "role": "user",
        "content": f"Context:\n{context}\n\nQuestion: {query.question}"
    })

    answer = await query_llm(messages)
    return {"answer": answer}
