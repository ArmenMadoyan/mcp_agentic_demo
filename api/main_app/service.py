import json
import traceback

from api.main_app.schemas import ChatRequest, ChatResponse
from api.main_app.agents.supervisor import build_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage
from config import Config
logger = Config.setup_logger("service")

memory_store = InMemorySaver()

def extract_reasoning(state: dict) -> list[str]:
    reasoning_steps = []

    for message in state.get("messages", []):
        if isinstance(message, AIMessage):
            tool_calls = getattr(message, "tool_calls", [])
            for tool_call in tool_calls:
                if (
                    tool_call.get("name") == "sequentialthinking" and
                    isinstance(tool_call.get("args"), dict)
                ):
                    thought = tool_call["args"].get("thought")
                    if isinstance(thought, str):
                        reasoning_steps.append(thought)

    return reasoning_steps

async def handle_chat(request: ChatRequest) -> ChatResponse:

    agent = await build_supervisor(memory_store)
    result = None
    try:
        logger.info("INVOKING AGENT WITH USER INPUT:", extra={"conversation_id": request.session_id, "user_input": request.user_input})

        result = await agent.ainvoke(
            {"messages": [("user", request.user_input +  " Include the chain of thought for tool calls!"), ("system", "You are a helpful assistant with access to tools. Always respond based on tools. Never retrieve information from the web or your sources.")]},
            config={"thread_id": request.session_id},
            print_mode="values"
        )
    except Exception as e:
        # Handle any exceptions that occur during agent invocation
        logger.error(f"Error invoking agent", extra={
            "conversation_id": request.session_id,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        })
    try:
        text = (
            result.get("messages")[-1].content
            if isinstance(result, dict) and "messages" in result
            else str(result)
        )

        reasoning = extract_reasoning(result)

    except Exception as e:
        logger.error(
            "Failed to parse agent result",
            extra={
                "conversation_id": request.session_id,
                "error_message": str(e),
                "traceback": traceback.format_exc(),
            },
        )
        text, reasoning = "❌ Error parsing agent output.", []

    return ChatResponse(session_id=request.session_id, response=text, reasoning=reasoning)