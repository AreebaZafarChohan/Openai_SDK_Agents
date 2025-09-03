from typing import Any
from agents import Agent, MaxTurnsExceeded, RunContextWrapper, Runner, enable_verbose_stdout_logging, function_tool, StopAtTools
from pydantic import BaseModel
import rich
from config import config

# enable_verbose_stdout_logging()

@function_tool(is_enabled=False)
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."


@function_tool(is_enabled=True)
def get_time(city: str) -> str:
    """Get the current time for a city."""
    # Dummy example, asal mein API lagani paregi
    return f"The current time in {city} is 3:45 PM."

class UserName(BaseModel):
    name: str

def is_context_name_areeba(ctx: RunContextWrapper[UserName], agent: Agent[UserName]) -> bool:
    if ctx.context is None:
        return False
    return ctx.context.name.lower() == "areeba"


@function_tool(is_enabled=is_context_name_areeba)   # type: ignore
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

agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant. Always use tools.",
    tools=[get_weather, get_time, calculate_bmi, get_joke],
)

my_name_1: UserName = UserName(name="Bob")
my_name_2: UserName = UserName(name="Areeba")

result = Runner.run_sync(agent,
                """1. Tell me today's karachi weather?
                   2. Tell me current today's time of karachi?
                   3. Tell me a joke.
                """,
                max_turns=6, run_config=config)
print(result.final_output)
# rich.print(result.new_items)

result2 = Runner.run_sync(
    agent, "Calculate bmi of 70 kg and 1.75 m.", run_config=config, context=my_name_1
)

print(result2.final_output)

result3 = Runner.run_sync(
    agent, "Calculate bmi of 70 kg and 1.75 m.", run_config=config, context=my_name_2
)

print(result3.final_output)
rich.print(result3.new_items)