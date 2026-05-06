import os
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()


API_KEY = os.getenv("CHATGPT_API_KEY")

# # Initialiazing the Client

client = OpenAI(api_key=API_KEY)

previous_response_id = None



web_search_choice = input("do you want the response from web search?(yes/no)?").strip().lower()

if web_search_choice =="yes":
    tools = [{"type":"web_search_preview"}]
else:
    tools = None

print("\nI'm your tech career counsellor. Type 'quit' to exit.\n")
                  
INSTRUCTION="""
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

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "quit":
        print("Good luck on your tech journey!")
        break
    if not user_input:
        continue

    response = client.responses.create(
        model="gpt-4.1",
        instructions=INSTRUCTION,
        input=user_input,
        tools=tools,
        previous_response_id=previous_response_id,  # chains history
    )
    previous_response_id = response.id

    print(f"\nCounsellor: {response.output_text}\n")

