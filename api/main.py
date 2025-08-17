import asyncio

from fastapi import FastAPI
from api.main_app.routes import router
import uvicorn
import sys
import os

from config import Config

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = FastAPI(
    title="Agentic Ops API",
    description="LangGraph-based multi-agent API with memory and monitoring.",
    version="0.1.0",
)


# Include the /chat route
app.include_router(router)

app.state.model_lock = asyncio.Lock()
app.state.llm = Config.set_model("gpt-4o")

# Run the app directly
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
