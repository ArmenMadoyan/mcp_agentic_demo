from api.main_app.schemas import ChatRequest, ChatResponse
from api.main_app.agents.supervisor import get_supervisor_agent
from langgraph.checkpoint.memory import InMemorySaver

# (1) Create a memory store tied to this session
memory_store = InMemorySaver()

# (2) Load the LangGraph agent with memory
agent = get_supervisor_agent(memory_store)

async def handle_chat(request: ChatRequest) -> ChatResponse:
    # (3) Run the agent with the user's message
    result = await agent.ainvoke(
        {"input": request.user_input},
        config={"thread_id": request.session_id}
    )
    # if result is dict with messages, grab last AI text
    text = (
        result.get("messages")[-1].content
        if isinstance(result, dict) and "messages" in result
        else str(result)
    )
    # (4) Return structured response
    return ChatResponse(session_id=request.session_id, response=text)