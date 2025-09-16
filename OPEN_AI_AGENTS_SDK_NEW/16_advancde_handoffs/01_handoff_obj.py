from agents import Agent, RunContextWrapper, Runner, function_tool, handoff
from config import config

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."

def on_handoff(context: RunContextWrapper):
    print(f"\n[SYSTEM: Handoff initiated. Briefing: '{context}']\n")
    
news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You get latest news about tech community and share it with me.",
    tools=[get_weather],
)

weather_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are weather expert - share weather updates as I travel a lot. For all Tech and News let the NewsAgent handle that part by delegation.",
    tools=[get_weather],
    handoffs=[handoff(agent=news_agent, on_handoff=on_handoff)]
)

res = Runner.run_sync(weather_agent, "Check if there's any news about OpenAI after GPT-5 launch?", run_config=config)
print("\nAGENT NAME", res.last_agent.name)
print("\n[RESPONSE:]", res.final_output)
