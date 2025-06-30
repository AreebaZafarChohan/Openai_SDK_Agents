import os
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner, function_tool
from openai import AsyncOpenAI
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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

@function_tool
def get_weather(city: str) -> str:
    """
    Get the weather for a given city.
    """
    result = requests.get(f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}")
    
    if result.status_code == 200:
        data = result.json()
        return f"The weather in {city} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data."

agent: Agent = Agent(
    name="Weather Agent",
    instructions="You are a weather agent. You can provide weather information and forecasts.",
    tools=[get_weather]
)

result = Runner.run_sync(agent, "What's the weather like in Karachi?", run_config=config)
print(result.final_output)
