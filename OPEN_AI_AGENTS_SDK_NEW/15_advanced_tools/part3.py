import asyncio
from agents import Agent, MaxTurnsExceeded, ModelSettings, RunContextWrapper, function_tool, Runner
from config import config
from dataclasses import dataclass

@dataclass
class UserScope:
    is_admin: bool
    
async def is_weather_allowed(ctx: RunContextWrapper[UserScope], agent: Agent[UserScope]) -> bool:
    print(f"Checking weather permission for admin: {ctx.context}")
    return True if ctx.context.is_admin else False

@function_tool(is_enabled=is_weather_allowed) # type: ignore
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather in {city} is sunny."

base_agent: Agent = Agent(
    name="Base Agent",
    instructions="Provide information about the weather. Always use tools",
    tools=[get_weather],
    model_settings=ModelSettings(tool_choice="required"),
    tool_use_behavior="stop_on_first_tool"
)

async def main():
    user_scope = UserScope(is_admin=False)
    admin_scope = UserScope(is_admin=True)
    
    res = await Runner.run(base_agent, "What is weather in lahore?",run_config=config, context=user_scope)
    print(f"Final Output: {res.final_output}")
    
    res2 = await Runner.run(base_agent, "What is weather in lahore?",run_config=config, context=admin_scope)
    print(f"Final Output: {res2.final_output}")
    
if __name__ == "__main__":
    asyncio.run(main())
