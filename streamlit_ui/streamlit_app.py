# streamlit_ui/streamlit_app.py

import streamlit as st
import requests

st.title("💬 Chatbot (Lambda + Bedrock)")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Lambda APIのエンドポイント
    api_url = "https://xxx.execute-api.us-east-1.amazonaws.com/Prod/chat"  # デプロイ後に置き換え

    try:
        res = requests.post(api_url, json={"messages": st.session_state.messages})
        res.raise_for_status()
        msg = res.json()["completion"]
        st.session_state["messages"].append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
    except Exception as e:
        st.error(f"Error: {e}")
