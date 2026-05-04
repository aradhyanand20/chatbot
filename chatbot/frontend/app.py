import streamlit as st

st.title("Tech counsellor Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_window = st.container()
with chat_window:
    for msg in st.session_state.messages:
        with st.chat_message([msg["role"]]):
            st.write(msg["content"])

with st.form(key="chats", clear_on_submit=True):
    user_input = st.text_input("Enter you message:",placeholder="what you want to ask?")
    send = st.form_submit_button("submit")

if send and user_input.strip():
    st.session_state.messages.append({"role":"user", "content":user_input})
    st.rerun()