# 🤖 Tech Counsellor Chatbot

An AI-powered career counselling chatbot that provides real-time, personalized tech career guidance — built with GPT-4.1, FastAPI, and Streamlit.

---

## ✨ Features

- 🎯 **Personalized career roadmaps** — tailored advice based on your skills, experience level, and goals
- 🌐 **Live web search** — fetches up-to-date salary data, job trends, and course recommendations
- ⚡ **Real-time streaming** — responses stream token by token for a natural, ChatGPT-like experience
- 💬 **Persistent chat history** — full conversation context maintained throughout the session
- 🧠 **Expert persona** — powered by a carefully crafted system prompt simulating 15+ years of tech industry experience

---

## 🏗️ Architecture

```
┌─────────────────────┐        HTTP POST (streaming)        ┌──────────────────────┐
│                     │  ─────────────────────────────────▶│                       │
│   Streamlit UI      │       /chatting endpoint           |   FastAPI Backend     │
│   (frontend.py)     │ ◀───────────────────────────────── │   (main.py)          │
│                     │     token chunks (text/plain)       │                      │
└─────────────────────┘                                     └──────────┬───────────┘
                                                                       │
                                                                       │ calls
                                                                       ▼
                                                            ┌──────────────────────┐
                                                            │   LLM Layer          │
                                                            │   (new_llm.py)       │
                                                            │                      │
                                                            │  • GPT-4.1           │
                                                            │  • System prompt     │
                                                            │  • Web search tool   │
                                                            └──────────────────────┘
```

---

## 📁 Project Structure

```
tech-counsellor-chatbot/
│
├── new_llm.py          # LLM layer — GPT-4.1 streaming client with system prompt & web search
├── main.py             # FastAPI backend — exposes /chat and /chatting REST endpoints
├── frontend.py         # Streamlit UI — chat interface with real-time token streaming
├── .env                # Environment variables (API keys) — never commit this
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tech-counsellor-chatbot.git
cd tech-counsellor-chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
CHATGPT_API_KEY=your_openai_api_key_here
```

### 4. Start the FastAPI backend

```bash
uvicorn main:app --reload
```

The API will be live at `http://127.0.0.1:8000`.

### 5. Launch the Streamlit frontend

Open a new terminal and run:

```bash
streamlit run frontend.py
```

The chatbot UI will open at `http://localhost:8501`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Standard blocking chat — returns full response as JSON |
| `POST` | `/chatting` | Streaming chat — streams tokens in real time as `text/plain` |

### Request body (both endpoints)

```json
{
  "message": "How do I become a machine learning engineer?"
}
```

### `/chat` response

```json
{
  "reply": "Great question! Here's a roadmap to becoming an ML engineer..."
}
```

### `/chatting` response

A streaming `text/plain` response — chunks arrive progressively as the model generates them.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **LLM** | GPT-4.1 via OpenAI Responses API |
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | Streamlit |
| **Streaming** | OpenAI streaming + `requests` iter_content |
| **Web Search** | OpenAI `web_search_preview` tool |
| **Config** | python-dotenv |

---

## 🧩 Module Breakdown

### `new_llm.py` — LLM Layer
Handles all communication with the OpenAI API. Contains:
- The **system prompt** that defines the counsellor's persona, expertise, and tone
- The `stream_chat()` generator function that streams GPT-4.1 responses token by token
- The **web search tool** integration for live data lookups

### `main.py` — FastAPI Backend
Exposes two HTTP endpoints:
- **`/chat`** — a simple blocking endpoint for testing; returns the full model response at once
- **`/chatting`** — the production endpoint; wraps `stream_chat()` in a `StreamingResponse` for real-time output

### `frontend.py` — Streamlit UI
Provides the chat interface:
- Maintains conversation history in `st.session_state` across reruns
- Uses `st.empty()` + in-place `placeholder.markdown()` updates to simulate live typing
- Appends a `▌` cursor while streaming to signal the model is still generating

---

## 💡 How Streaming Works

```
User submits message
       │
       ▼
Streamlit POSTs to /chatting with stream=True
       │
       ▼
FastAPI passes message to stream_chat() generator
       │
       ▼
OpenAI streams tokens → FastAPI forwards each chunk immediately
       │
       ▼
Streamlit reads chunks via iter_content() in a loop
       │
       ├─ each chunk: full_text += chunk → placeholder updates with "▌" cursor
       │
       ▼
Stream ends → final markdown rendered, cursor removed
       │
       ▼
Full reply saved to session_state → st.rerun()
```

---

## ⚠️ Important Notes

- **Never commit your `.env` file.** Add it to `.gitignore` immediately.
- The `/chat` endpoint does **not** use the system prompt or web search — it is intended for quick testing only. Use `/chatting` for the full counsellor experience.
- `previous_response_id` in `new_llm.py` is scaffolded but not yet wired up. Connecting it would enable true multi-turn memory across API calls.

---

## 🔮 Potential Improvements

- [ ] Wire up `previous_response_id` for persistent multi-turn conversation memory
- [ ] Add user authentication to support multiple independent sessions
- [ ] Persist chat history to a database (e.g., PostgreSQL, SQLite)
- [ ] Migrate frontend input to `st.chat_input()` for a more native chat UX
- [ ] Add support for file uploads (resume review feature)
- [ ] Deploy backend on Railway / Render and frontend on Streamlit Cloud
- [ ] Switch to `claude-sonnet` or other models via a config flag

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [OpenAI](https://openai.com) for the GPT-4.1 API and web search tooling
- [FastAPI](https://fastapi.tiangolo.com) for the blazing-fast Python web framework
- [Streamlit](https://streamlit.io) for making Python UIs effortless