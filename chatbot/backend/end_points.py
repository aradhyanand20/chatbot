from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))

class ChatRequest(BaseModel):
    message: str

def stream_chat(message: str):
    with client.responses.stream(
        model="gpt-4.1",
        input=message,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta


@app.post("/chat")
def chat(req:ChatRequest):
    print(req.message)
    response = client.responses.create(
        model= "gpt-4.1",
        input = req.message
    )
    return {"reply": response.output[0].content[0].text}


@app.post("/chatting")
def chat(req: ChatRequest):
    return StreamingResponse(
        stream_chat(req.message),
        media_type = "text/plain"
    )
    