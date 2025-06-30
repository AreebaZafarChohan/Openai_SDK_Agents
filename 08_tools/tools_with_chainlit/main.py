import os
from dotenv import load_dotenv
from typing import cast, List
import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.run import RunConfig
from agents.tool import function_tool
import httpx

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("OPENWEATHER_API_KEY") 

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.set_starters # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",
        ),
        cl.Starter(
            label="Weather",
            message="Find the weather in Karachi",
        ),
    ]
    

@function_tool
@cl.step(type="weather tool") # type: ignore
def get_weather(location: str, unit: str = "C"):
    """
     Fetch real-time weather for a given location using OpenWeatherMap API.
    """
    if not API_KEY:
        return "API key not found. Please set OPENWEATHER_API_KEY in your environment."
    
    # convert unit
    units_param = "metric" if unit.upper() == "C" else "imperial"
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units={units_param}"
    
    try:
        response = httpx.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return f"Error: {data.get('message', 'Failed to fetch weather')}"
        
        temp = data['main']['temp']
        description = data['weather'][0]['description'].capitalize()
        city = data['name']
        
        return f"🌤️ Weather in {city}: {temp}°{unit.upper()} — {description}."
    
    except Exception as e:
        return f"Error fetching weather: {e}"

@cl.on_chat_start
async def start():
    
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client, # type: ignore
        tracing_disabled=True
    )
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    
    cl.user_session.set("chat_history", [])
    
    cl.user_session.set("config", config)
    
    agent: Agent = Agent(name="Assitant", instructions="You are a helpful assistant.")
    agent.tools.append(get_weather)
    
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Welcome to the Areeba's AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """
    Process incoming messages and generate responses.
    """    
    
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()
    
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    
    # Retrieve the chat history from the session.
    
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        
        msg.content = response_content
        await msg.update()
        
         # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": response_content})
        # NOTE: Here we are appending the response to the history as a developer message.
        # This is a BUG in the agents library.
        # The expected behavior is to append the response to the history as an assistant message.
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", history)
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")    
