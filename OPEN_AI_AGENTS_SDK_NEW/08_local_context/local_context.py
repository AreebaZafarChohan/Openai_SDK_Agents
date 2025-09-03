import asyncio
from dataclasses import dataclass
from turtle import st
from agents import Agent, Runner, RunContextWrapper, function_tool, enable_verbose_stdout_logging
from config import config


# enable_verbose_stdout_logging()

@dataclass
class UserInfo:
    name: str
    id: int
    location: str
    age: int
    
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Returns the user's age."""
    return f"User '{wrapper.context.name}' is '{wrapper.context.age}' years old."


@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Returns the user's location."""
    return f"User '{wrapper.context.name}' is from '{wrapper.context.location}'."

async def main():
    
    user_info = UserInfo(name="Areeba Zafar", id=7, location="Karachi, Pakistan", age=20)
    
    agent: Agent = Agent[UserInfo](
        name="Assistant",
        instructions="You are a helping assistant.",
        tools=[fetch_user_age, fetch_user_location]
    )
    
    result = await Runner.run(
        agent,
        "What is the age of user and his/her location?",
        run_config=config,
        context=user_info,
    )
    
    print("Local Context [RunContextWrapper]")
    print(result.final_output)
    print("="*70)
    
if __name__ == "__main__":
    asyncio.run(main())    
    
    
    
    

        