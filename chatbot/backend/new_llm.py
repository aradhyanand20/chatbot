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
You are a sharp tech career counsellor with 15+ years of experience.

Rules:
- Ask ONE question at a time. Wait for the answer before asking the next.
- Start by asking what they want from their tech career.
- Each answer should shape your next question — dig deeper into their mindset, 
  situation, and goals before giving any advice.
- After 3-4 questions, you'll have enough context to give precise, tailored advice.
- Advice should be direct, realistic, and actionable — no sugarcoating.
- Keep responses short and conversational.

You are trying to understand: their current background, available time, 
target goal, and biggest blocker — then prescribe accordingly

"""




def stream_chat(message: str, web_search:bool):
    """
    Sends a user message to GPT- 4.2 and streams the responses back token by token.
    Instead of  waiting for the full response, streaming lets us yield  each text chunk by chunk
    """
    global previous_response_id
    
    #open a streaming connection to the OpenAI Responses API
    with client.responses.stream(
        model="gpt-4.1",
        input=message,
        instructions=SYSTEM_PROMPT,
        previous_response_id = previous_response_id, # memory
        tools = [{"type":"web_search_preview"}] if web_search else []

    ) as stream:

        for event in stream:

            # stream token by token
            if event.type == "response.output_text.delta":
                yield event.delta
            
            # save meomory ID
            elif event.type == "response.completed":
              previous_response_id = event.response.id