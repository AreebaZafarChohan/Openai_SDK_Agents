from agents import Agent, RunContextWrapper, Runner, function_tool, handoff
from pydantic import BaseModel
from config import config


class NewsRequest(BaseModel):
    topic: str
    reason: str

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

def on_news_transfer(ctx: RunContextWrapper, input_data: NewsRequest) -> None:
    print(f"\nTransferring to for news updates. input_data:", input_data, "\n")

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me.",
    tools=[get_weather],
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are weather expert - share weather updates as I travel a lot. For all Tech and News let the NewsAgent handle that part by delegation.",
    tools=[get_weather],
    handoffs=[handoff(agent=news_agent, on_handoff=on_news_transfer, input_type=NewsRequest)]
)

res = Runner.run_sync(weather_agent, "Check if there's any news about OpenAI after GPT-5 launch?", run_config=config)
print("\nAGENT NAME", res.last_agent.name)
print("\n[RESPONSE:]", res.final_output)