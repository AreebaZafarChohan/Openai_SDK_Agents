from agents import Agent, Runner, function_tool
from config import config

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    tools=[get_weather]
)

new_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    tools=[get_weather]
)

res = Runner.run_sync(base_agent, "What's the weather in Karachi?", run_config=config)
print(res)