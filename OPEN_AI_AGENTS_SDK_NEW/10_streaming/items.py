import asyncio
from config import config
from agents import Agent, ItemHelpers, RunResultStreaming, Runner, function_tool
from openai.types.responses import ResponseTextDeltaEvent
import random 

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)

async def main():
    agent: Agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes]
    )
    
    result : RunResultStreaming = Runner.run_streamed(
        agent,
        input="Hii.",
        run_config= config,
    )
    
    print("\n","**"*50)
    print("\n=== Run Starting ===\n")
    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent Updated {event.new_agent.name}")
            continue
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool Output: {event.item.output}")
                # print(f"\n --- {event.item.raw_item}")
            elif event.item.type == "message_output_item":
                print(f"-- Message Output: \n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass           

try:
    asyncio.run(main())            
except:
    pass

print("=== Run Complete ==")    