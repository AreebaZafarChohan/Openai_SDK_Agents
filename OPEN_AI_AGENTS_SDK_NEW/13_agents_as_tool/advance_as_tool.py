import asyncio
from unittest import result
from config import config
from agents import Agent, RunResult, Runner, function_tool


@function_tool
def get_weather():
  return "It is sunny"

weather_agent:Agent = Agent(
      name="weather checker",
      instructions="Use avaible tools get weather info",
      tools=[get_weather],
  )

@function_tool
async def weather_agent_fun(query: str) -> str:
    result: RunResult = await Runner.run(weather_agent, query, max_turns=3, run_config=config)
    return result.final_output

agent :Agent = Agent(
    name="General Agent",
    instructions="Answer general purpose query efficently if tool call is require call available tools",
    tools=[weather_agent_fun],
)


async def main():
    result = await Runner.run(agent, "What is the weather like today of karachi?", run_config=config)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())