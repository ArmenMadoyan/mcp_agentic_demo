import traceback

from api.main_app.schemas import ChatRequest, ChatResponse
from api.main_app.agents.supervisor import build_supervisor
from langgraph.checkpoint.memory import InMemorySaver

# (1) Create a memory store tied to this session
memory_store = InMemorySaver()

async def handle_chat(request: ChatRequest) -> ChatResponse:
    # (2) Load the LangGraph agent with memory
    agent = await build_supervisor(memory_store)
    # (3) Run the agent with the user's message
    try:
        print("INVOKING AGENT WITH USER INPUT:", request.user_input)
        result = await agent.ainvoke(
            {"messages": [("user", request.user_input)]},
            config={"thread_id": request.session_id},
            print_mode="values"
        )
    except Exception as e:
        # Handle any exceptions that occur during agent invocation
        print(f"Error invoking agent: {e}")
        print(traceback.format_exc())
    # if result is dict with messages, grab last AI text
    text = (
        result.get("messages")[-1].content
        if isinstance(result, dict) and "messages" in result
        else str(result)
    )
    # (4) Return structured response
    return ChatResponse(session_id=request.session_id, response=text)