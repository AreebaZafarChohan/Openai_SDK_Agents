import asyncio
from agents import Agent, MaxTurnsExceeded, function_tool, StopAtTools, Runner
from config import config

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather in {city} is sunny."

base_agent: Agent = Agent(
    name="Base Agent",
    instructions="Provide information about the weather and travel plans.",
    tools=[get_weather],
)

async def main():
    try:
        res = await Runner.run(base_agent, "What is weather in lahore?", run_config=config, max_turns=2)
        print(f"Final Output: {res.final_output}")
        
        res2 = await Runner.run(base_agent, "What is weather in lahore?", run_config=config, max_turns=1)
        print(f"Final Output: {res2.final_output}")
    except MaxTurnsExceeded as e:
        print(f"Max turns exceeded: {e}")

if __name__ == "__main__":
    asyncio.run(main())
