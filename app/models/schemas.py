from pydantic import BaseModel
from typing import List, Optional

class ChatQuery(BaseModel):
    question: str
    namespace: str
    user_id: str
    history: Optional[List[dict]] = None
