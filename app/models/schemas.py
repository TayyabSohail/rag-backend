from pydantic import BaseModel

class ChatQuery(BaseModel):
    question: str
    namespace: str
