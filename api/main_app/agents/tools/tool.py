# /api/main_app/agents/tools/tool.py

from typing import Any
from langchain_core.tools import Tool
import logging

logger = logging.getLogger(__name__)


class BaseTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def _run(self, query: str) -> Any:
        raise NotImplementedError("Subclasses must implement _run method.")

    def __call__(self, query: str) -> Any:
        logger.info(f"Calling tool [{self.name}] with query: {query}")
        try:
            result = self._run(query)
            logger.info(f"Tool [{self.name}] response: {result}")
            return result
        except Exception as e:
            logger.exception(f"Error in tool [{self.name}]: {e}")
            return f"Error: {str(e)}"

    def as_langchain_tool(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            func=self.__call__,
        )
