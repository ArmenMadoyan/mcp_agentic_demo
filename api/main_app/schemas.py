from typing import List
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    user_input: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    reasoning: List[str]

class Message(BaseModel):
    role: str
    content: str

class InjectedState(BaseModel):
    messages: list[Message]
    conversation_id: str | None = None
