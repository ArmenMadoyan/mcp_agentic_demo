from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path='.env', override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')
model = os.getenv('MODEL_NAME')

class Config:
    LANGSMITH_API_KEY = langsmith_api_key

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
            api_key=api_key,
        )
        return llm