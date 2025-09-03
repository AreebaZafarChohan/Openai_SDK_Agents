import asyncio
from config import config
from agents import Agent, RunResultStreaming, Runner
from openai.types.responses import ResponseTextDeltaEvent

async def main():
    agent: Agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )
    
    result : RunResultStreaming = Runner.run_streamed(
        agent,
        input="Please tell me 5 jokes.",
        run_config= config,
    )
    
    print("\n","**"*50)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

asyncio.run(main())            