import asyncio
from agents import Agent, enable_verbose_stdout_logging, handoff, RunContextWrapper, Runner
from config import config

enable_verbose_stdout_logging()

urdu_agent = Agent(
    name="Urdu agent",
    instructions="You only speak Urdu."
)

english_agent = Agent(
    name="English agent",
    instructions="You only speak English"
)

def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    agent_name = agent.name
    print("--------------------------------")
    print(f"Handing off to {agent_name}...")
    print("--------------------------------")


triage_agent = Agent(
    name="Triage agent",
    instructions="Handoff to the appropriate agent based on the language of the request.",
    handoffs=[
            handoff(urdu_agent, on_handoff=lambda ctx: on_handoff(urdu_agent, ctx)),
            handoff(english_agent, on_handoff=lambda ctx: on_handoff(english_agent, ctx))
    ],
)


async def main(input: str):
    result = await Runner.run(triage_agent, input=input, run_config=config)
    print(result.final_output)

asyncio.run(main("Hello, how are you?"))  