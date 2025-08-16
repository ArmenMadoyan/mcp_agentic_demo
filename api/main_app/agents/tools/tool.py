import abc
import asyncio
from typing import Any, Callable
from langchain_core.tools import Tool
import logging

logger = logging.getLogger(__name__)


class BaseTool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abc.abstractmethod
    async def _arun(self, query: str) -> Any:
        raise NotImplementedError("Subclasses must implement _run method.")

    async def __call__(self, query: str) -> Any:
        logger.info("Calling tool [%s] with query: %s", self.name, query)
        try:
            result = await self._arun(query)
            logger.info("Tool [%s] response: %s", self.name, str(result)[:500])
            return result
        except Exception as e:
            logger.exception("Error in tool [%s]: %s", self.name, e)
            return f"Error: {str(e)}"

    def as_langchain_tool(self) -> Tool:
        """
        Provides both async and sync entrypoints:
        - LangChain will use `coroutine` when available.
        - `func` is a safe sync wrapper for callers that lack async (rare).
        """
        async_fn: Callable[[str], Any] = self.__call__

        def _sync_wrapper(q: str) -> Any:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None
            if loop and loop.is_running():
                # If already in a running loop, run in a new task and block
                return asyncio.run(async_fn(q))  # simplest, safe for CLI/dev
            return asyncio.run(async_fn(q))

        return Tool(
            name=self.name,
            description=self.description,
            func=_sync_wrapper,
            coroutine=async_fn,
        )
