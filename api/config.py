from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env', override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
langsmith_api_key = os.getenv('LANGSMITH_API_KEY')
claude_api_key = os.getenv('CLAUDE_API_KEY')

class Config:
    OPENAI_API_KEY = openai_api_key
    LANGSMITH_API_KEY = langsmith_api_key
    CLAUDE_API_KEY = claude_api_key