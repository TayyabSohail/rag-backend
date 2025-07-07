from fastapi import APIRouter
from app.models.schemas import ChatQuery
from app.services.embedder import model
from app.services.vector_store import query_similar_chunks
from app.services.llm_client import query_llm

router = APIRouter()

@router.post("/")
async def chat(query: ChatQuery):
    query_vec = model.encode([query.question]).tolist()[0]
    chunks = query_similar_chunks(query_vec, namespace=query.namespace)
    context = "\n".join(chunks)
    
    full_prompt = f"Answer based on the context below:\n\n{context}\n\nQuestion: {query.question}"
    answer = await query_llm(full_prompt)
    return {"answer": answer}
