from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from config import Config

model = Config.set_model(model_name='gpt-4o')

async def build_supervisor(memory_store: InMemorySaver):
    # 1) create the client
    client = MultiServerMCPClient(
        {
            "wikipedia": {
                "transport": "sse",
                "url": "http://localhost:8080/sse"
            },
        }
    )

    # 3) fetch tools (LangChain Tool objects)
    tools = await client.get_tools()
    print(111111, tools)
    # 4) wire into your agent
    agent = create_react_agent(model, tools=tools, checkpointer=memory_store)

    return agent