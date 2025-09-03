from os import name
from config import config
from agents import Agent, ModelSettings, Runner


base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# simple clone

friendly_agent = base_agent.clone(
    name="FriendlyAgent",
    instructions="You are a very friendly and warn assistant.",
)

query = "Hello, how are you?"

result_base = Runner.run_sync(base_agent, query, run_config=config)
result_friendly = Runner.run_sync(friendly_agent, query, run_config=config)

print("Base Agent:", result_base.final_output)
print("Friendly Agent:", result_friendly.final_output)