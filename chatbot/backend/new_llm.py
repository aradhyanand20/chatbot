from openai import OpenAI
from dotenv import load_dotenv
import os
from prompts import BASE_PROMPT, WEB_ENABLED_PROMPT, WEB_DISABLED_PROMPT

# loading the .env file and intializing the OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))


#track the ID of previous API response
previous_response_id = None


def stream_chat(message: str, web_search: bool):
    """
        Sends a user message to GPT-4.1 and streams the responses back token by token.
        Instead of  waiting for the full response, streaming lets us yield  each text chunk by chunk
        """
    global previous_response_id

    system_prompt = BASE_PROMPT + (WEB_ENABLED_PROMPT if web_search else WEB_DISABLED_PROMPT)

    #open a streaming connection to the OpenAI Responses API
    with client.responses.stream(
        model="gpt-4.1",
        input=message,
        instructions=system_prompt,
        previous_response_id=previous_response_id,  # memory
        tools=[{"type": "web_search_preview"}] if web_search else [],
    ) as stream:

        for event in stream:

            # stream token by token
            if event.type == "response.output_text.delta":
                yield event.delta

            # save meomory ID
            elif event.type == "response.completed":
                previous_response_id = event.response.id


def stream_chat_with_resume(message: str, conversation_history: list, resume_text: str = None):
    """
    Streams a response that maintains full conversation history
    and optionally keeps resume context throughout the session.
    """

    full_input = ""

    if resume_text:
        full_input += f"""
         The user has shared their resume. Use it throughout our conversation to give
         personalized advice. Here is the resume content:

         --- RESUME START ---
         {resume_text}
         --- RESUME END ---"""

    for turn in conversation_history:
        role = "User" if turn["role"] == "user" else "Assistant"
        full_input += f"{role}:{turn['content']}\n"

    full_input += f"User: {message}"

    with client.responses.stream(
        model="gpt-4.1",
        input=full_input,
        instructions=BASE_PROMPT + WEB_ENABLED_PROMPT,
        tools=[{"type": "web_search_preview"}],
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
