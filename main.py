import asyncio

import streamlit as st

from data_fetcher import fetch_wash_type_data
from db import init_db, close_db
from model_generator import generate_source_code
from optiguide_agent import create_agent_and_user


def run_async(coro):
    return asyncio.run(coro)


async def process_question(question, api_key):
    await init_db()
    try:
        wash_type_data = await fetch_wash_type_data()
        print("wash_type_data", wash_type_data)
        source_code = generate_source_code(wash_type_data)
        agent, user = create_agent_and_user(source_code, api_key=api_key)
        ans = user.initiate_chat(agent, message=question)
        return ans.summary
    finally:
        await close_db()


# Sidebar for API key input
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API key:", type="password")

# Main app layout
st.title("Laundry Optimization with OptiGuide")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


question = st.text_input("Enter your question about laundry optimization:")

if st.button("Ask OptiGuide") and question.strip() and api_key.strip():
    with st.spinner("Processing your question..."):
        summary = run_async(process_question(question, api_key))
        st.session_state.chat_history.append({"question": question, "response": summary})

st.markdown("### Chat History")
for chat in st.session_state.chat_history:
    st.markdown(f"**You:** {chat['question']}")
    st.markdown(f"**OptiGuide:** {chat['response']}")
