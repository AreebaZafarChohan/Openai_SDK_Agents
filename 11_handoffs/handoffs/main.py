import asyncio
from agents import Agent, Runner
from config import config

billing_agent = Agent(
    name="Billing Agent",
    instructions="You handle all billing-related inquiries. Provide clear and concise information regarding billing issues."
)

refund_agent = Agent(
    name="Refund Agent",
    instructions="You handle all refund-related processes. Assist users in processing refunds efficiently."
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent should handle the user's request based on the nature of the inquiry.",
    handoffs=[billing_agent, refund_agent]
)

async def main():
    user_input="I need a refund for my recent purchase."
    
    result = await Runner.run(triage_agent, user_input, run_config=config)
    print(result.final_output)

asyncio.run(main())    