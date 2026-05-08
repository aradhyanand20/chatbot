from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req:ChatRequest):
    response = client.responses.create(
        model= "gpt-4.1",
        input = req.message
    )
    return {"reply": response.output[0].content[0].text}