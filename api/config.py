from dotenv import load_dotenv
import os
import logging
import sys
from pythonjsonlogger import json
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv(dotenv_path='.env', override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')

class Config:
    LANGSMITH_API_KEY = langsmith_api_key

    @staticmethod
    def setup_logger(name=__name__, level=logging.INFO):
        # JSON formatter (minimal fields, can expand if needed)
        formatter = json.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s %(conversation_id)s %(user_id)s"
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers = [handler]
        logger.propagate = False
        return logger

    @staticmethod
    def set_model(model_name: str = 'gpt-4o'):

        if model_name.lower().strip() == 'claude-2':
            model_name = 'claude-2'
            api_key = claude_api_key
        else:
            api_key = openai_api_key

        llm = ChatOpenAI(
            model=model_name,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key= SecretStr(api_key),
        )
        return llm