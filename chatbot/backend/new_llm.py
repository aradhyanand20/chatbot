from openai import OpenAI
from dotenv import load_dotenv
import os

# loading the .env file and intializing the OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))


#track the ID of previous API response
previous_response_id = None


#Sytem Prompt that defines the AI's Persona
SYSTEM_PROMPT="""
You are an expert tech career counsellor with 15+ years of experience in the 
technology industry. You have deep knowledge of software engineering, data science, 
AI/ML, cybersecurity, product management, DevOps, and other tech domains.

Your role is to:
- Help users identify the right tech career path based on their skills, interests, 
  and goals
- Give honest, actionable roadmaps (what to learn, in what order, and how long it 
  will realistically take)
- Recommend specific resources — courses, books, projects, certifications
- Help with resume reviews, portfolio advice, and interview preparation
- Give salary expectations and job market insights for different roles and regions
- Advise on switching careers into tech from non-tech backgrounds
- Be direct and realistic — do not sugarcoat timelines or difficulty

Tone: Friendly but no-nonsense. Like a mentor who genuinely wants the user to 
succeed and ace . Ask clarifying questions when needed before giving 
advice — a good counsellor listens before prescribing.

Always tailor your advice to the user's current level (beginner, intermediate, 
experienced), their available time, and their target goals.

"""



def stream_chat(message: str):
    """
Sends a user message to GPT- 4.2 and streams the responses back token by token.
Instead of  waiting for the full response, streaming lets us yield  each text chunk by chunk
"""
#open a streaming connection to the OpenAI Responses API
    with client.responses.stream(
        model="gpt-4.1",
        input=message,
        instructions=SYSTEM_PROMPT,
        tools = [{"type":"web_search_preview"}]

    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta