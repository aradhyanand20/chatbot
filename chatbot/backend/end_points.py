from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from new_llm import stream_chat


# load environment variables from .env
load_dotenv()

#FastAPI application instance
app = FastAPI()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))

#pydantic model
class ChatRequest(BaseModel):
    message: str
    web_search:bool = False


#Endpoint 1: standard chat
@app.post("/chat")
def chat(req:ChatRequest):
    """
    A basic, non-streaming chat endpoint.
    Simpler to implement, but the client has to wait until the
    model finishes generating — no real-time feel
    """
    print(req.message)
    response = client.responses.create(
        model= "gpt-4.1",
        input = req.message
    )
    return {"reply": response.output[0].content[0].text}

#Endpoint 2: Streaming chat
@app.post("/chatting")
def chat(req: ChatRequest):
    """
    A streaming chat endpoint that uses the counsellor persona from new_llm.py.
    Instead of waiting for the full response, it streams tokens back to the client
    as they are generated — giving a real-time 'typing' effect.
    Uses StreamingResponse to push each chunk over the HTTP connection progressively
    rather than buffering everything and sending it all at once.
    """
    return StreamingResponse(
        stream_chat(
        req.message,
        req.web_search
        ),
        media_type = "text/plain"
    )
    