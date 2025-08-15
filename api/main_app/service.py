from api.main_app.schemas import ChatRequest, ChatResponse
from api.main_app.agents.supervisor import get_supervisor_agent
from langgraph.checkpoint.memory import InMemorySaver

# (1) Create a memory store tied to this session
memory_store = InMemorySaver()

async def handle_chat(request: ChatRequest) -> ChatResponse:

    # (2) Load the LangGraph agent with memory
    agent = get_supervisor_agent(memory_store)

    # (3) Run the agent with the user's message
    result = await agent.ainvoke(
        {"input": request.user_input},
        configurable={"thread_id": request.session_id}
    )
    # (4) Return structured response
    return ChatResponse(
        session_id=request.session_id,
        response=result
    )
