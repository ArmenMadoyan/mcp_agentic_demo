from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph
from langgraph.checkpoint import BaseSaver

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableConfig

from api.main_app.agents.tools.wikipedia import WikipediaTool
from api.main_app.agents.tools.wolfram import WolframTool

from config import Config
model = Config.set_model(model_name='gpt-4o')

# Define the list of tools (agents) available to the supervisor
tools = [WikipediaTool, WolframTool]

# Entry + Exit keys for the LangGraph flow
class AgentState(dict):
    pass

def get_supervisor_agent(memory_store: BaseSaver):
    # React agent from LangChain with tool usage
    react_agent = create_react_agent(
        tools=tools,
        llm="openai/gpt-4",  # replace with LangChain LLM if using LC integration
        prompt="You are a helpful agentic assistant using tools to help the user."
    )

    # Create stateful LangGraph
    builder = StateGraph(AgentState)
    builder.add_node("agent", react_agent)
    builder.set_entry_point("agent")
    builder.set_finish_point("agent")

    app = builder.compile()

    # Return the runnable graph with memory
    return app.with_configurable(configurable={"memory": memory_store})
