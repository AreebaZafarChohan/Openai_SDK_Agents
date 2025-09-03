from config import config
from agents import Agent, ModelSettings, Runner, function_tool

@function_tool
def calculate_area(length: float, width: float) -> str:
    return f"Area = {length * width} square units"

@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 72°F"

# Base agent with one tool
base_agent = Agent(
    name="BaseAssistant",
    tools=[calculate_area],
    instructions="You are a helpful assistant."
)

# Clone with additional tool
weather_agent = base_agent.clone(
    name="WeatherAssistant",
    tools=[calculate_area, get_weather],  # New tools list
    instructions="You are a weather and math assistant."
)

# Clone with different tools
math_agent = base_agent.clone(
    name="MathAssistant",
    tools=[calculate_area],  # Same tools
    instructions="You are a math specialist."
)

query = "Tell me today's weather of karachi and calculate the area 25cm width and 40cm length."

result_weather_agent = Runner.run_sync(weather_agent, query, run_config=config)
result_math_agent = Runner.run_sync(math_agent, query, run_config=config)


print("\nweather Agent:", result_weather_agent.final_output)
print("\n", "==="*50)
print("\nMath Agent:", result_math_agent.final_output)