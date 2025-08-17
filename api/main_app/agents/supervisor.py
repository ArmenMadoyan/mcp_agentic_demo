import traceback

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from config import Config

model = Config.set_model(model_name='gpt-4o')
logger = Config.setup_logger("supervisor")

async def build_supervisor(memory_store: InMemorySaver):
    client = MultiServerMCPClient(
        {
            "wikipedia": {
                "transport": "sse",
                "url": "http://localhost:8080/sse"
            },
            "sequentialthinking": {
                "transport": "stdio",
                "command": "docker",
                "args": [
                    "run",
                    "--rm",
                    "-i",
                    "mcp/sequentialthinking"
                ]
            }
        }
    )

    try:
        logger.info("Supervisor gathering the tools")
        tools = await client.get_tools()
    except Exception as e:
        logger.error("Failed to gather tools", extra={
            "error_message": str(e),
            "traceback": traceback.format_exc()
        })
        return None


    agent = create_react_agent(model, tools=tools, checkpointer=memory_store)

    return agent