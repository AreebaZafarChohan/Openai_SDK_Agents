import asyncio
from dataclasses import dataclass
from turtle import st
from agents import Agent, Runner, RunContextWrapper, function_tool, enable_verbose_stdout_logging
from config import config


# enable_verbose_stdout_logging()

@dataclass
class UserContext:
    username: str
    email: str | None = None
    
@function_tool
async def search(local_ctx: RunContextWrapper[UserContext], query: str) -> str:
    import time
    time.sleep(30) # Simulating a delay for the search operation
    # return "No results found."
    username = local_ctx.context.username  # User ka naam lena
    return f"Search results for '{query}': {local_ctx.context.username} is the best math tutor in this area."

async def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    print(f"\nUser: {special_context.context},\nAgent: {agent.name}\n")
    return (
        f"You are a math expert. "
        f"When the user asks any question that involves searching, always call the 'search' tool. "
        f"User: {special_context.context.username}, Agent: {agent.name}."
    )

math_agent: Agent =Agent(
    name="Genius",
    instructions=special_prompt,
    tools=[search]
)    

# [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

async def call_agent():
    # Call the agent with a specific input
    
    user_context: UserContext = UserContext(username="Areeba Zafar")
    
    output = await Runner.run(
        starting_agent=math_agent,
        input="Search for the best math tutor in my area",
        context=user_context,
        run_config=config,
    )
    
    print(f"\n\nOutput: {output.final_output}\n\n")

asyncio.run(call_agent())    
    
    
    
    

        