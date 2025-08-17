import traceback

from fastapi import APIRouter, HTTPException
from api.main_app.service import handle_chat
from api.main_app.schemas import ChatRequest, ChatResponse
from config import Config

router = APIRouter()
logger = Config.setup_logger("chat")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        logger.info("User message received", extra={"conversation_id": request.session_id})
        return await handle_chat(request)

    except HTTPException as e:
        logger.error("HTTP Exception occurred", extra={
            "conversation_id": request.session_id,
            "error_message": str(e.detail),
            "traceback": traceback.format_exc()
        })
        return ChatResponse(session_id=request.session_id, response="Error in backend " + str(e), reasoning=[])

    except Exception as e:
        # unexpected errors -> 500
        logger.error("Unknown Exception occurred", extra={
            "conversation_id": request.session_id,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        })
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
