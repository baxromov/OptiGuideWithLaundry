import streamlit as st
import asyncio

from db import init_db, close_db
from data_fetcher import fetch_wash_type_data
from model_generator import generate_source_code
from optiguide_agent import create_agent_and_user

def run_async(coro):
    return asyncio.run(coro)

async def process_question(question):
    await init_db()
    try:
        wash_type_data = await fetch_wash_type_data()
        print("wash_type_data", wash_type_data)
        source_code = generate_source_code(wash_type_data)
        agent, user = create_agent_and_user(source_code)
        ans = user.initiate_chat(agent, message=question)
        return ans.summary
    finally:
        await close_db()

st.title("Laundry Optimization with OptiGuide")

question = st.text_input("Enter your question about laundry optimization:")

if st.button("Ask OptiGuide") and question.strip():
    with st.spinner("Processing your question..."):
        summary = run_async(process_question(question))
        st.markdown("### Agent's Response")
        st.text(summary)
