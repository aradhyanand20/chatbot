import streamlit as st
import requests
from streamlit_mic_recorder import mic_recorder

#APP Title
st.title("Tech counsellor Chatbot")


#  Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

#chat History Display
chat_window = st.container()

with chat_window:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Voice Input Section
st.subheader("🎤 Voice Input")

audio = mic_recorder(
    start_prompt = "🎙 Start Recording",
    stop_prompt = "⏹ Stop Recording",
    just_once=True,
    use_container_width=True,
)

# Sending the recorded audio to the backend

if audio:
    files = {
        "file" : ("audio.wav",audio["bytes"],"audio/wav")
    }

    with st.spinner("Transcribing audio..."):

        response = requests.post(
            "http://localhost:8000/transcribe",
            files=files
        )
    
    if response.status_code == 200:
        print(response.json())
        st.session_state.voice_text = response.json()["text"]
        
        st.success("✅ Transcription completed!")

        st.rerun()
    
    else:
        st.error("❌ Transcription failed")



#User Input Form
with st.form(key="chats", clear_on_submit=True):
    user_input = st.text_input(
        "Enter you message:",
        value = st.session_state.voice_text,
        placeholder="what you want to ask?"
    )

    # web search toggle
    web_search = st.checkbox("🌐 Use Web Search")
    
    send = st.form_submit_button("submit")

#Handle Submission & Stream Response
if send and user_input.strip():

    # Clear voice text after submit
    st.session_state.voice_text = ""

    # store user message
    st.session_state.messages.append({"role":"user", "content":user_input})


# Render the assistant's chat bubble
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        # show initial loading state
        placeholder.markdown("Thinking...")

# POST to the streaming FastAPI endpoint
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
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()