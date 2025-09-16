from config import config
from agents import Agent, Runner, handoff, RunContextWrapper, function_tool
from agents.extensions import handoff_filters
from pydantic import BaseModel
import asyncio

# --- Define the data for our "briefing note" ---
class HandoffData(BaseModel):
    summary: str

# --- Define our specialist agents ---
billing_agent = Agent(
    name="Billing Agent",
    instructions="Handle billing questions."
)

technical_agent = Agent(
    name="Technical Support Agent",
    instructions="Troubleshoot technical issues."
)

# --- Define our on_handoff callback ---
def log_the_handoff(ctx: RunContextWrapper, input_data: HandoffData):
    print(f"\n[SYSTEM: Handoff initiated. Briefing: '{input_data.summary}']\n")

# --- Create the advanced handoffs ---
# Billing handoff
to_billing_handoff = handoff(
    billing_agent,
    tool_name_override="transfer_to_billing",
    on_handoff=log_the_handoff,
    input_type=HandoffData
)

# Technical handoff
to_technical_handoff = handoff(
    technical_agent,
    on_handoff=log_the_handoff,
    input_type=HandoffData,
    input_filter=handoff_filters.remove_all_tools 
)

# --- Triage Agent uses the handoffs ---
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "First, use the 'diagnose' tool. Then, based on the issue, "
        "handoff to the correct specialist with a summary."
    ),
    tools=[
        # Dummy diagnostic tool
        function_tool(lambda: "The user's payment failed.", name_override="diagnose")
    ],
    handoffs=[to_billing_handoff, to_technical_handoff],
)


async def main():
    print("--- Running Scenario: Billing Issue ---")
    result = await Runner.run(triage_agent, "My payment won't go through.", run_config=config)
    print(f"Final Reply From: {result.last_agent.name}")
    print(f"Final Message: {result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())

