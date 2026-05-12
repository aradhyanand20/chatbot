from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from openai import OpenAI
import os
import io
import json
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from new_llm import stream_chat, stream_chat_with_resume


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
    
    #endpoint 3: RESUME TEXT EXTRACTOR

@app.post("/upload-resume")
async def upload_resume(file: UploadFile= File(...)):

    file_bytes =  await file.read()

    if file.filename.endswith(".pdf"):
        try:
            import pypdf
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_bytes))
            resume_text = "\n".join(
                page.extract_text() for page in pdf_reader.pages if page.extract_text()
            )
        except Exception as e:
            return {"error":f"failed to read PDF:{str(e)}"}
        
    else:
        try:
            resume_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            return {"error": "Unsupported format. Please upload a PDF,TXT OR MD file"}
    
    return {"resume_text": resume_text}

#Endpoint 4
@app.post("/chat_with_resume")
async def chat_with_resume(
    message: str = Form(...),
    conversation_history: str = Form(...),
    resume: str = Form(default="")
):
    history =json.loads(conversation_history)

    return StreamingResponse(
        stream_chat_with_resume(
            message=message,
            conversation_history=history,
            resume_text=resume if resume else None  # Pass None if no resume uploaded
        ),
        media_type="text/plain"
    )

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...)
):
    try:

        #read uploaded audio
        audio_bytes = await file.read()

        temp_file = "temp_audio.wav"

        # Save temporary audio file
        with open(temp_file, "wb") as f:
            f.write(audio_bytes)

        # Open audio for whisper
        with open(temp_file, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(
                model = "whisper-1",
                file = audio_file
            )
        
        # Delete temp file
        os.remove(temp_file)

        return {
            "text": transcript.text
        }

    except Exception as e:

        return {
            "error": str(e)
        }