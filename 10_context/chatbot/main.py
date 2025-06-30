from typing import List, cast
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI
import os
from agents.run_context import RunContextWrapper
from agents.run import RunConfig
import chainlit as cl
import requests

# load env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY") 


BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

print(f"Loaded API Key: {OPENROUTER_API_KEY is not None}")

# check API KEY is existing or not
if not OPENROUTER_API_KEY:
    raise ValueError("Please ensure that your OPENROUTER_API_KEY is set in .env file.")


# set starting messages
@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi.",
        ),
    ]


class MyContext:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.seen_messages = []

# create a function tools         

# this is the weather function tool without context
@function_tool
@cl.step(type="weather tool") # type: ignore
def get_weather(location: str, unit: str = "C") -> str:
    """
    Get the weather for a given city.
    """
    
    result = requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={location}")
    
    if result.status_code == 200:
        data = result.json()
        return f"The weather in {location} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."
    
@function_tool
@cl.step(type="greeting tool") # type: ignore
def greet_user(context: RunContextWrapper[MyContext], greeting: str) -> str:
    user_id = context.context.user_id
    return f"Hello {user_id}, you said: {greeting}"   
    
    
# setup chat starting message and setup session with creating model, external client and config also with creating agent    

@cl.on_chat_start
async def start():
    # Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url=BASE_URL,
    )

    model = OpenAIChatCompletionsModel(
        model=MODEL, openai_client=external_client
    )

    config = RunConfig(
        model=model, model_provider=external_client, tracing_disabled=True # type: ignore
    )
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    agent: Agent = Agent(
        name="Areeba's Assistant",
        tools=[greet_user, get_weather],
        instructions="You are a helpful assistant. Call greet_user tool to greet the user. Always greet the user when session starts.",
        model=model,
    )

    cl.user_session.set("agent", agent)

    await cl.Message(
        content="Welcome to the Areeba's AI Assistant! How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []

    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    my_ctx = MyContext(user_id="Areeba")

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config, context=my_ctx)

        response_content = result.final_output

        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": response_content})

        # Update the session with the new history.
        cl.user_session.set("chat_history", history)

        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")