import json
import traceback

from api.main_app.schemas import ChatRequest, ChatResponse
from api.main_app.agents.supervisor import build_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage


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
        print("INVOKING AGENT WITH USER INPUT:", request.user_input)
        result = await agent.ainvoke(
            {"messages": [("user", request.user_input + "! Include your reasoning!"), ("system", "You are a helpful assistant with access to tools. Always respond based on tools. Never retrieve information from the web or your sources.")]},
            config={"thread_id": request.session_id},
            print_mode="values"
        )
    except Exception as e:
        # Handle any exceptions that occur during agent invocation
        print(f"Error invoking agent: {e}")
        print(traceback.format_exc())

    text = (
        result.get("messages")[-1].content
        if isinstance(result, dict) and "messages" in result
        else str(result)
    )

    reasoning = extract_reasoning(result)

    return ChatResponse(session_id=request.session_id, response=text, reasoning=reasoning)