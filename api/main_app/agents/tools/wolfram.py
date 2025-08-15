from api.external.mcp_wolfram.main import ask_wolfram  # Adjust if entry point differs
from api.main_app.agents.tools.tool import BaseTool

class WolframTool(BaseTool):
    def invoke(self, input: str) -> str:
        # Add logging here if needed
        return ask_wolfram(input)
