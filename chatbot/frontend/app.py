import streamlit as st
import requests

st.title("Tech counsellor Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_window = st.container()
with chat_window:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

with st.form(key="chats", clear_on_submit=True):
    user_input = st.text_input("Enter you message:",placeholder="what you want to ask?")
    send = st.form_submit_button("submit")

if send and user_input.strip():
    st.session_state.messages.append({"role":"user", "content":user_input})

    # # Adding a 2 second loading
    # with st.spinner("Thinking..."):
    #     import time
    #     time.sleep(2)

    # ---------------------------------

    # response = requests.post(
    #     "http://127.0.0.1:8000/chat",
    #     json= {"message": user_input}
    # )

    # print(response.json())

    # # genarate a bot reply
    # # bot_reply = f"You said {user_input}"
    # bot_reply = response.json()["reply"]

    # -----------------------------------


    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        # show initial loading state
        placeholder.markdown("Thinking...")

        response = requests.post(
            "http://127.0.0.1:8000/chatting",
            json={"message": user_input},
            stream = True # required for streaming
        )

        #stream tokens
        for chunk in response.iter_content(
            chunk_size = None,
            decode_unicode=True
        ):
            if chunk:
                full_text += chunk
                placeholder.markdown(full_text + "▌")


        # final response
        placeholder.markdown(full_text)
        bot_reply = full_text

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()