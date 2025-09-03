import asyncio
from agents import Agent, Runner, enable_verbose_stdout_logging, trace
from config import config

enable_verbose_stdout_logging()


async def main():
    agent: Agent = Agent(
        name="Joke generator",
        instructions="You are a joke generator. Tell me a joke.",
    )
    
    with trace("Joke Workflow"):
        first_result = await Runner.run(agent, "Tell me a joke", run_config=config)
        second_result = await Runner.run(agent, f"Rate this joke: {first_result.final_output}", run_config=config)
        
        print(f"Joke: {first_result.final_output}")
        print(f"Rating: {second_result.final_output}")

asyncio.run(main())