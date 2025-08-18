# mcp_agentic_demo

# 🧠 Agentic LLM System Demo

## 🚀 Purpose

This project demonstrates a **modular agentic system** using [LangGraph](https://github.com/langchain-ai/langgraph) to coordinate LLM tools, memory, and runtime model flexibility in a production-style environment.

The agent acts as a reasoning engine that can dynamically interact with external tools (e.g., Wikipedia MCP), retain memory across turns, and expose both API and UI interfaces.

---


## ✅ Setup

```bash
```r
# 1. Clone the repository with submodules
git clone --recurse-submodules git@github.com:ArmenMadoyan/mcp_agentic_demo.git
cd mcp_agentic_demo/external/mcp_wikipedia

# --- Start Wikipedia MCP Server ---
uv venv && source .venv/bin/activate
uv sync
uv run wikipedia-mcp --transport sse --host 0.0.0.0 --port 8080

# --- Start Backend ---
# (From root: mcp_agentic_demo)
cd ../..
uv venv && source .venv/bin/activate
uv sync

# Create .env file with:
# OPENAI_API_KEY=your_key_here
# or
# CLAUDE_API_KEY=your_key_here

PYTHONPATH=api uv run -m main

# --- Start Frontend ---
# (From root: mcp_agentic_demo)
uv run streamlit run frontend/app.py
```

## ✅ Features & Results

- 🧩 **Agent Orchestration**
  - Built with `create_react_agent` using LangGraph
  - State machine behavior and memory checkpointing via `InMemorySaver`

- 🔄 **Runtime Model Switching**
  - `/set_model` API and UI selector to toggle between:
    - `gpt-4o` (OpenAI)
    - `gpt-3.5-turbo` (OpenAI)
    - `claude-2` (Anthropic)

- 🧠 **Memory Tracing**
  - Agent memory persists across conversation turns
  - `print_state=True` logs LLM input/output during debug

- 🔧 **Tool Integration**
  - Wikipedia MCP microservice (`uv run wikipedia-mcp`)
  - Agent leverages external tools to answer queries agentically

- ⚠️ **Robust Error Handling**
  - Catches and logs OpenAI key errors (401), missing tools, internal exceptions
  - Structured logging includes `conversation_id`, `traceback`, and message content

- 🖥️ **Frontend UI**
  - Streamlit interface for:
    - Messaging the agent
    - Choosing models dynamically
    - Observing real-time interaction and memory flow

---

## 📊 Key Learnings

- LangGraph agents require **explicit message management** to persist memory state across turns.
- Model and tool initialization should be **validated early and logged explicitly**.
- **Separation of concerns** between agent logic, web server, and UI is critical for maintainability.
- Custom structured logging is an effective lightweight alternative to a full ELK stack for local development.

---

## 📌 Note

LangSmith tracing is designed for enhanced observability and experiment tracking, but this demo uses `print_state=True` for lightweight debugging. The system is ready for integration with LangSmith or other observability layers when desired.
