from agents import Agent, HandoffInputData, RunContextWrapper, Runner, function_tool, handoff
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from config import config

def summarized_news_transfer(data: HandoffInputData) -> HandoffInputData:
    print("\n\n[HANDOFF] Summarizing news transfer...\n\n")
    summarized_conversation = "Get latest tech news."
    
    return HandoffInputData(
        input_history=summarized_conversation,
        pre_handoff_items=(),
        new_items=(),
    )

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me. Always transfer back to WeatherAgent after answering the questions",
)

planner_agent: Agent = Agent(
    name="PlannerAgent",
    instructions="You get latest news about tech community and share it with me. Always transfer back to WeatherAgent after answering the questions",
)

def news_region(region: str):
    def is_news_allowed(ctx: RunContextWrapper, agent: Agent) -> bool:
        return True if ctx.context.get("is_admin", False) and region == "us-east-1" else False
    return is_news_allowed

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions=f"You are weather expert - share weather updates as I travel a lot. For all Tech and News let the NewsAgent handle that part by delegation. {RECOMMENDED_PROMPT_PREFIX}",
    handoffs=[handoff(agent=news_agent, is_enabled=news_region("us-east-1")), planner_agent]
)

res = Runner.run_sync(weather_agent, 
                      "Check if there's any news about OpenAI after GPT-5 launch - also what's the weather SF?", 
                      context={"is_admin": True}
                      , run_config=config)
                      
print("\nAGENT NAME", res.last_agent.name)
print("\n[RESPONSE:]", res.final_output)
print("\n[NEW_ITEMS:]", res.new_items)