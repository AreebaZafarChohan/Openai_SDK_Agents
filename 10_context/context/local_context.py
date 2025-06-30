import asyncio
from agents import Agent, Runner, RunContextWrapper, function_tool
from dataclasses import dataclass

from config import config

@dataclass
class UserInfo:
    uid: int
    age: int
    name: str = "Areeba Chohan"
    location: str = "Karachi, Pakistan"
    
@function_tool
async def fetch_user_data(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Returns the name and age of the user."""
    
    return f"User {wrapper.context.name} is {wrapper.context.age} years old."

@function_tool
async def fetch_user_location(wrapper: RunContextWrapper[UserInfo]) -> str:
    """Returns the user's location."""
    
    return f"User {wrapper.context.name} is from {wrapper.context.location}."

async def main():
    user_info = UserInfo(name="Areeba Zafar", uid=715, age=19)
    
        
    agent = Agent[UserInfo](
        name="Assistant",
        tools=[fetch_user_data, fetch_user_location],
        instructions="You ae a helpful assistant. Always use tools 'fetch_user_data' and 'fetch_user_location'."
    )
    
    result = await Runner.run(
        starting_agent=agent,
        input="What is the user's age, name and location?",
        run_config=config,
        context=user_info
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())    
 