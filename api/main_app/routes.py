import traceback

from fastapi import APIRouter, HTTPException, Request
from api.main_app.service import handle_chat
from api.main_app.schemas import ChatRequest, ChatResponse
from config import Config

router = APIRouter()
logger = Config.setup_logger("chat")

@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest):
    try:
        llm = request.app.state.llm
        logger.info("User message received", extra={"conversation_id": body.session_id})
        return await handle_chat(body, llm)

    except HTTPException as e:
        logger.error("HTTP Exception occurred", extra={
            "conversation_id": body.session_id,
            "error_message": str(e.detail),
            "traceback": traceback.format_exc()
        })
        return ChatResponse(session_id=body.session_id, response="Error in backend " + str(e), reasoning=[])

    except Exception as e:
        logger.error("Unknown Exception occurred", extra={
            "conversation_id": body.session_id,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        })
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/set_model")
async def set_model_route(model_name: str, request: Request):
    async with request.app.state.model_lock:
        try:
            logger.info("Setting model", extra={"model_name": model_name})
            request.app.state.llm = Config.set_model(model_name)
        except Exception as e:
            logger.error("Failed to set model", extra={
                "model_name": model_name,
                "error_message": str(e),
                "traceback": traceback.format_exc()
            })
            raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True, "model": model_name}
