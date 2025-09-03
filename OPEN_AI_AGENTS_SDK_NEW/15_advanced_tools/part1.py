from agents import Agent, function_tool, StopAtTools, Runner
from config import config

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather in {city} is sunny."

@function_tool
def get_travel_plan(city: str) -> str:
    """A simple function to get a travel plan for a user."""
    return f"Travel plan is not available."

base_agent: Agent = Agent(
    name="Base Agent",
    instructions="Provide information about the weather and travel plans.",
    tools=[get_weather, get_travel_plan],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_travel_plan"])
)

res = Runner.run_sync(base_agent, "make me travel plan for lahore", run_config=config)
print(f"Final Output: {res.final_output}")

