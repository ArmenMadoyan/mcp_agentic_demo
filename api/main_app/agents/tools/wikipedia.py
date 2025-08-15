# /api/main_app/agents/tools/wikipedia.py

from api.main_app.agents.tools.tool import BaseTool
import wikipedia


class WikipediaTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="WikipediaSearch",
            description="Searches Wikipedia for a summary of a given topic."
        )

    def _run(self, query: str) -> str:
        return wikipedia.summary(query, sentences=2)
