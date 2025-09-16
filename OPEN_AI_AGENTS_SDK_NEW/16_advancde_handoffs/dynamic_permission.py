import asyncio
from agents import Agent, Runner, handoff
from pydantic import BaseModel
from config import config

class UserContext(BaseModel):
    user_id: str
    subscription_tier: str = "free"  # free, premium, enterprise
    has_permission: bool = False


# This agent will use the custom LLM provider
agent = Agent(
    name="Assistant",
    instructions="You only respond for the user's request and delegate to the expert agent if needed.",
   
)

expert_agent = Agent(
    name="Expert",
    instructions="You are an expert in the field of recursion in programming.",
)


agent.handoffs = [handoff(expert_agent, is_enabled=lambda ctx, agent: ctx.context.has_permission)]

async def main():
    context = UserContext(user_id="123", subscription_tier="premium", has_permission=False)

    result = await Runner.run(
        agent,
        "Call the expert agent and ask about recursion in programming",
        context=context,
        run_config=config
    )
    print(result.final_output)
    print(result.last_agent.name)


if __name__ == "__main__":
    asyncio.run(main())