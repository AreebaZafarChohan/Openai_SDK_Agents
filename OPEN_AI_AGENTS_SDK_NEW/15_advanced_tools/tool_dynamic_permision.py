import asyncio
from pydantic import BaseModel
from agents import RunContextWrapper, Agent, Runner, function_tool
from config import config

class UserContext(BaseModel):
    user_id: str
    subscription_tier: str = "free"
    has_permission: bool = False


def premium_feature_enabled(context: RunContextWrapper, agent: Agent) -> bool:
    print(f"premium_feature_enabled()")
    print(context.context.subscription_tier, context.context.subscription_tier in ["premium", "enterprise"])
    return context.context.subscription_tier in ["premium", "enterprise"]

@function_tool(is_enabled=premium_feature_enabled) # type: ignore
def get_weather(city: str) -> str:
    print(f"[ADV] get_weather()")
    return "Weather is sunny"


base_agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpfull agent.",
    tools=[get_weather],
    # model_settings=ModelSettings(tool_choice="required"),
    # tool_use_behavior="stop_on_first_tool"
)
    
async def main():
    context = UserContext(
        user_id="123",
        subscription_tier="premium",
        has_permission=True
    )
    print("--- First Run ---")
    res = await Runner.run(base_agent, "Call the get_weather tool with city 'London'", run_config=config, context=context)
    print(f"Final Output: {res.final_output}")

    # print("\n--- Second Run ---")
    # res2 = await Runner.run(base_agent, "What is the full form of AI?", run_config=config, context=context)
    # print(f"Final Output: {res2.final_output}")
    
if __name__ == "__main__":
    asyncio.run(main())
    
       