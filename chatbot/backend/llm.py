import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from openai import OpenAI



load_dotenv()


API_KEY = os.getenv("CHATGPT_API_KEY")

# # Initialiazing the Client

client = OpenAI(api_key=API_KEY)


                  
INSTRUCTION="""
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

def run_counsellor(user_input: str, previous_response_id: str= None, web_search: bool =False):
    tools = [{"type":"web_search_preview"}] if web_search else None

    def stream():
     with client.responses.stream(
        model="gpt-4.1",
        instructions=INSTRUCTION,
        input=user_input,
        tools=tools,
        previous_response_id=previous_response_id,
     ) as s:
        for  event in s:
           if event.type == "response.output_text.delta":
              yield f"data:{event.delta}\n\n"

        final = s.get_final_response()
        yield f"event: done\ndata: {final.id}\n\n"
        
        
 
    
    

    return StreamingResponse(stream(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no",
    })

  

# if __name__ == "__main__":
#     previous_response_id = None

#     print("Tech Career Counsellor (type 'quit' to exit)\n")

#     while True:
#         user_input = input("You: ").strip()

#         if user_input.lower() == "quit":
#             break
#         if not user_input:
#             continue


        
#         with client.responses.stream(
#             model="gpt-4.1",
#             instructions=INSTRUCTION,
#             input=user_input,
#             previous_response_id=previous_response_id,
            
#         ) as s:
#             print("Counsellor: ", end="", flush=True)
#             for event in s:
#                 if event.type == "response.output_text.delta":
#                     print(event.delta, end="", flush=True)  # prints token by token
            
#             previous_response_id = s.get_final_response().id  # chain history
#             print("\n")