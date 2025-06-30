from agents import enable_verbose_stdout_logging

from config import model
enable_verbose_stdout_logging()

import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

@dataclass
class UserInfo:
    name: str
    uid: int

@function_tool
async def greet_user(context: RunContextWrapper[UserInfo], greeting: str) -> str:
  """Greets the User with their name.
  Args:
    greeting: A specialed greeting message for user
  """
  name = context.context.name
  return f"Hello {name}, {greeting}"

async def main():
    user_info = UserInfo(name="Areeba", uid=715)

    agent = Agent[UserInfo](
        name="Assistant",
        tools=[greet_user],
        model=model,
        instructions="Always greet the user using greet_user."
    )

    result = await Runner.run(
        starting_agent=agent,
        input="Hello",
        context=user_info,
    )

    print(result.final_output)

asyncio.run(main())