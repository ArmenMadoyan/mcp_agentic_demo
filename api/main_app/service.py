from api.main_app.schemas import ChatRequest, ChatResponse

async def handle_chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(
        session_id=request.session_id,
        response="hello"
    )
