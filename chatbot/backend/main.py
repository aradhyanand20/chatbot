import os
from dotenv import load_dotenv
from openai import OpenAI



load_dotenv()


API_KEY = os.getenv("CHATGPT_API_KEY")

# # Initialiazing the Client
#
client = OpenAI(api_key=API_KEY)

user_input = input("I am Jesus😇"
                   "\nWhat you wanna know my child!\n\n"
                   "Your question-> ")

# # Call the Chat Completion API
response = client.responses.create(
    model="gpt-4.1",
    input= user_input
)

print(response.output[0].content[0].text)