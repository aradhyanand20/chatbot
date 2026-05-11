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

When a resume is provided:
- Start by summarizing what you see: current skills, experience level, and background
- Identify skill gaps for the user's target role
- Give a personalized step-by-step roadmap based specifically on THEIR resume
- Reference specific things from their resume when giving advice

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

def stream_chat_with_resume(message:str, conversation_history:list, resume_text: str = None):
    """
    Streams a response that maintains full conversation history
    and optionally keeps resume context throughout the session. 
    """

    full_input = ""

    if resume_text:
        full_input +=f"""
         The user has shared their resume. Use it throughout our conversation to give 
         personalized advice. Here is the resume content:

         --- RESUME START ---
         {resume_text}
         --- RESUME END ---"""
        
    for turn in conversation_history:
        role= "User" if turn["role"] == "user" else "Assistant"
        full_input += f"{role}:{turn['content']}\n"
    
    full_input += f"User: {message}"

    with client.responses.stream(
        model="gpt-4.1",
        input=full_input,
        instructions= SYSTEM_PROMPT,
        tools=[{"type": "web_search_preview"}]
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta

        
    


