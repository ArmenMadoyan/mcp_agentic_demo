from dotenv import load_dotenv
import os
import logging
import sys
from pythonjsonlogger import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from pydantic import SecretStr
from pathlib import Path

# Resolve project root no matter where this file lives
ROOT = Path(__file__).resolve().parents[0]
# If this file is in api/, parents[1] is project root. If it’s in project root, keep parents[0].
if (ROOT / ".env").exists():
    DOTENV = ROOT / ".env"
else:
    DOTENV = Path(__file__).resolve().parents[1] / ".env"
# Load .env from project root, override anything stale
load_dotenv(dotenv_path=DOTENV, override=True)

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
        try:
            if model_name.lower().strip() == 'claude-2':
                model_name = 'claude-2'

                llm = ChatAnthropic(
                    model=model_name,
                    temperature=0,
                    max_tokens=1000,
                    timeout=60,
                    max_retries=2,
                    api_key=SecretStr(claude_api_key),
                )
            else:
                llm = ChatOpenAI(
                    model=model_name,
                    temperature=0,
                    max_tokens=1000,
                    timeout=60,
                    max_retries=2,
                    api_key= SecretStr(openai_api_key),
                )

            return llm
        except Exception as e:
            print("Please Set OPENAI_API_KEY or CLAUDE_API_KEY in .env file")
            raise e
