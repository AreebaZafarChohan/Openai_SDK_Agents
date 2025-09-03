from agents import Agent, MaxTurnsExceeded, Runner, enable_verbose_stdout_logging, function_tool, StopAtTools
import rich
from config import config

# enable_verbose_stdout_logging()

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


@function_tool
def get_time(city: str) -> str:
    """Get the current time for a city."""
    # Dummy example, asal mein API lagani paregi
    return f"The current time in {city} is 3:45 PM."


@function_tool
def calculate_bmi(weight: float, height: float) -> str:
    """Calculate Body Mass Index (BMI)."""
    bmi = weight / (height ** 2)
    return f"Your BMI is {bmi:.2f}, which is considered {'healthy' if 18.5 <= bmi <= 24.9 else 'unhealthy'}."


@function_tool
def get_joke() -> str:
    """Return a random joke."""
    jokes = [
        "Why don’t skeletons fight each other? They don’t have the guts.",
        "I told my computer I needed a break, and it said: 'No problem, I’ll go to sleep.'",
        "Why did the scarecrow win an award? Because he was outstanding in his field!"
    ]
    import random
    return random.choice(jokes)


weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. Always use tools",
    tools=[get_weather, get_time, calculate_bmi, get_joke],
    tool_use_behavior="run_llm_again"
)

multi_agent: Agent = Agent(
    name="MultiAgent",
    instructions="You are a helpfull agent.",
    tools=[get_weather, get_time, calculate_bmi, get_joke],
    tool_use_behavior="stop_on_first_tool",
)

mixed_agent: Agent = Agent(
    name="Mixed_Agent",
    instructions="You are a utility agent that only returns tool outputs directly.",
    tools=[get_joke, get_weather, get_time, calculate_bmi],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["get_weather", "calculate_bmi"]) # type: ignore
)

# "run_llm_again" Default behaviour
try:
    res1 = Runner.run_sync(weather_agent, "What's the weather in Karachi and what is my name?", run_config=config, max_turns=0)
    print(res1.final_output)
    rich.print(res1.new_items)
except MaxTurnsExceeded as e:
    print(f"Max turns exceeded, as expected. Error: {str(e)} | {type(str(e))} - {e} | {type(e)} ")  
    
# res1 = Runner.run_sync(weather_agent, "What's the weather in Karachi and what is my name?", run_config=config, max_turns=0)
# print(res1.final_output)
# rich.print(res1.new_items)      

# # "stop_on_first_tool"
# res2 = Runner.run_sync(multi_agent, "What's the current time in Karachi?", run_config=config)
# print(res2.final_output)
# rich.print(res2.new_items)

# # StopATTools
# res3 = Runner.run_sync(mixed_agent, "Tell me a joke and what is the current weather of karachi?", run_config=config)
# print(res3.final_output)
# rich.print(res3.new_items)
