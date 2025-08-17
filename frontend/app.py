import streamlit as st
import uuid
import requests

st.set_page_config(page_title="Wikipedia Agent", layout="centered")

# Session ID (once per user session)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("📚 Wikipedia Reasoning Agent")
st.markdown("Ask anything, and get step-by-step reasoning with an answer.")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages (everything already in history)
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("reasoning"):
            key = f"reasoning_{i}"
            if st.button("🧠 Show reasoning", key=key):
                st.markdown(msg["reasoning"])

user_input = st.chat_input("Ask your question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send to backend
    response = requests.post(
        "http://localhost:8000/chat",
        json={
            "session_id": st.session_state.session_id,
            "user_input": user_input
        },
        timeout=60,
    )

    if response.ok:
        data = response.json()
        st.session_state.messages.append(
            {"role": "agent", "content": data["response"], "reasoning": data.get("reasoning", "")}
        )
        with st.chat_message("agent"):
            st.markdown(data["response"])
            if data.get("reasoning"):
                if st.button("🧠 Show reasoning", key=f"reasoning_button_{len(st.session_state.messages)}"):
                    st.markdown(data["reasoning"])
    else:
        st.session_state.messages.append(
            {"role": "agent", "content": "Error from backend", "reasoning": ""}
        )
        with st.chat_message("agent"):
            st.markdown("❌ Error from backend")
