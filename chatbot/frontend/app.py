import streamlit as st
import requests
import json
#APP Title
st.title("Tech counsellor Chatbot")

#session State Intialization
if "message" not in st.session_state:
    st.session_state.messages = []

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

    
# sidebar resume Upload
with st.sidebar:
    st.header("📄 Your Resume")
    st.caption("Upload your resume to get personalized career advice")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf","txt","md"]
)

if uploaded_file is not None and not st.session_state.resume_uploaded:
    with st.spinner("reading your resume. . ."):
        response = requests.post(
            "http://127.0.0.1:8000/upload-resume",
            files={"file":(
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )}
        )
        result = response.json()

        if "resume_text" in result:
            st.session_state.resume_text = result["resume_text"]
            st.session_state.resume_uploaded = True
            st.success("✅ Resume uploaded!")
        else:
            st.error(f"❌ {result.get('error', 'Failed to read resume.')}")

if st.session_state.resume_uploaded:
    st.info("📎 Resume active — advice is personalized to you.")
    if st.button("🗑️ Remove Resume"):
        st.session_state.resume_text = ""
        st.session_state.resume_uploaded = False
        st.rerun()




#chat History Display
chat_window = st.container()
with chat_window:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


#User Input Form
with st.form(key="chats", clear_on_submit=True):
    user_input = st.text_input("Enter you message:",placeholder="what you want to ask?")

    # web search toggle
    web_search = st.checkbox("🌐 Use Web Search")
    
    send = st.form_submit_button("submit")

#Handle Submission & Stream Response
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

# Render the assistant's chat bubble
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        # show initial loading state
        placeholder.markdown("Thinking...")

# Route to correct endpoint based on whether resume exists
        if st.session_state.resume_text:
            # Resume uploaded → personalized endpoint
            response = requests.post(
                "http://127.0.0.1:8000//chat_with_resume",
                data={
                    "message": user_input,
                    "conversation_history": json.dumps(st.session_state.messages[:-1]),
                    "resume": st.session_state.resume_text
                },
                stream=True
            )
        else:
            response = requests.post(
            "http://127.0.0.1:8000/chatting",
            json={
                "message": user_input,
                "web_search": web_search
                },
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

 # Persist the assistant's full reply in session state for future reruns
    if bot_reply.strip():
        st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })



    