from config import config
import asyncio
from dataclasses import dataclass
from agents import Agent, Runner, RunContextWrapper, function_tool

# Define a simple context using a dataclass

@dataclass
class UserInfo:
    name: str
    uid: int
    

# A tool function that accesses local context via the wrapper
@function_tool
async def fetch_user_age(wrapper: RunContextWrapper[UserInfo]) -> str:
    return f"User {wrapper.context.name} is 19 years old"    

async def main():
    
    # create context object
    user_info = UserInfo(name="Areeba", uid=715)
    
    # Define an agent that with use the tool above
    agent = Agent[UserInfo](
        name="Areeba's Assistant",
        instructions="You must ALWAYS call the `fetch_user_age` function to answer any age-related question.",
        tools=[fetch_user_age],
    )
    
    # Run the agent, passing in the local context
    result = await Runner.run(
        starting_agent=agent,
        input="what is the user's age?",
        context=user_info,
        run_config=config
    )
    
    print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())
        