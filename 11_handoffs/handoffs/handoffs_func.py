import asyncio
from agents import Agent, Runner, handoff
from config import config

refund_agent = Agent(
    name="Refund Agent",
    instructions="You handle all refund-related processes."
)

# customize the handoff to the refund_agent

custom_handoff = handoff(
    agent=refund_agent,
    tool_name_override="custom_refund_handoff",
    tool_description_override="Handles refund processes with customized parameters."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent should handle the user's request.",
    handoffs=[custom_handoff]
)

async def main():
    user_input="I need a refund for my recent purchase."
    
    result = await Runner.run(triage_agent, user_input, run_config=config)
    print(result.final_output)

asyncio.run(main()) 