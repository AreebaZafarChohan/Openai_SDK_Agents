import asyncio
import os
from typing import Any
from agents import Agent, RunContextWrapper, AgentHooks, Runner, enable_verbose_stdout_logging
from config import config

enable_verbose_stdout_logging()

class TestAgHooks(AgentHooks):
    def __init__(self, ag_display_name):
        self.event_counter = 0
        self.ag_display_name = ag_display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} started. Usage: {context.usage}")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(f"### {self.ag_display_name} {self.event_counter}: Agent {agent.name} ended. Usage: {context.usage}, Output: {output}")

start_agent = Agent(
    name="Content Moderator Agent",
    instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
    hooks=TestAgHooks(ag_display_name="content_moderator"),
)

async def main():
  result = await Runner.run(
      start_agent,
      input=f"Will Agentic AI Die at end of 2025?.",
      run_config=config,
  )

  print(result.final_output)

asyncio.run(main())
print("--end--")
          