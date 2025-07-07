from fastapi import FastAPI
from app.routes import upload, chat

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def root():
    return {"message": "Snobbots RAG backend is running!"}
