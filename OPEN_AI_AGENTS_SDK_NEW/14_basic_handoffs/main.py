import asyncio
from unittest import result

import rich
from config import config
from agents import Agent, ReasoningItem, enable_verbose_stdout_logging, handoff, Runner

# enable_verbose_stdout_logging()

# 1) Two specialists that will OWN the conversation after transfer
billing_agent = Agent(
    name="Billing Agent",
    instructions="Resolve billing problems end-to-end. Ask for any details you need."
)

refunds_agent = Agent(
    name="Refunds Agent",
    instructions="Handle refunds end-to-end. Ask for order ID and explain next steps."
)

# 2) Triage agent that decides WHO should take over
triage = Agent(
    name="Triage Agent",
    instructions=(
        "Greet the user and decide where to send them:\n"
        "- If the user asks about a double charge, invoice, payment, etc., hand off to Billing Agent.\n"
        "- If the user asks about refund status or returning an item, hand off to Refunds Agent.\n"
        "Once handed off, the specialist should continue the conversation."
    ),
    # You can list the agents directly or wrap with handoff(...) for later customization
    handoffs=[billing_agent, handoff(refunds_agent, tool_name_override="refunds_tool", tool_description_override="Handles all refund-related inquiries.")],
)

async def main():
    # Example A: A refund-style question → should hand off to Refunds Agent
    r1 = await Runner.run(triage, "Hi, I returned my headset last week. What's my refund status?", run_config=config)
    print("A) Final reply (from REFUNDS specialist):", r1.final_output, "\n")
    # rich.print(r1.new_items)

    # Example B: A billing-style question → should hand off to Billing Agent
    r2 = await Runner.run(triage, "My card was charged twice for the same order.", run_config=config )
    print("B) Final reply (from BILLING specialist):", r2.final_output)
    # for item in r2.new_items:
    #     rich.print(type(item), item)
    # for item in r2.new_items:
    #     if isinstance(item, ReasoningItem):
    #         print("Reasoning mila:", item.raw_item)
if __name__ == "__main__":
    asyncio.run(main())