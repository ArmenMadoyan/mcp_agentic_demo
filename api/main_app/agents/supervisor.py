from typing import Annotated
from langgraph.prebuilt import create_react_agent, InjectedState
from langgraph.checkpoint.memory import InMemorySaver

from api.main_app.agents.tools.wikipedia import WikipediaTool
from config import Config

model = Config.set_model(model_name='gpt-4o')

# --- wrap classes into callable sub-agents ---
async def wikipedia_agent(state: Annotated[dict, InjectedState]) -> str:
    """Use the Wikipedia MCP sub-agent to fetch concise, factual summaries for the latest user message."""

    tool = WikipediaTool()
    query = state["messages"][-1].content  # latest user msg
    return await tool._arun(query)



def get_supervisor_agent(memory_store: InMemorySaver):
    # tools = sub-agents (functions)
    tools = [wikipedia_agent]

    supervisor = create_react_agent(
        model,
        tools=tools,
        checkpointer=memory_store
    )

    return supervisor