# Imports
import asyncio
from typing import Any
from config import config
from agents import Agent, RunContextWrapper, RunHooks, Runner

class TestHooks(RunHooks):
    def __init__(self):
        self.event_counter = 0
        self.name = "TestHooks"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")

start_hook = TestHooks()

start_agent = Agent(
    name="Content Moderator Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
)

async def main():
  result = await Runner.run(
      start_agent,
      hooks=start_hook,
      input=f"Will Agentic AI Die at end of 2025?.",
      run_config=config,
  )

  print(result.final_output)

asyncio.run(main())
print("--end--")     