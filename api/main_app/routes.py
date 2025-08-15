from fastapi import APIRouter
from api.main_app.service import handle_chat
from api.main_app.schemas import ChatRequest, ChatResponse
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    return await handle_chat(request)
