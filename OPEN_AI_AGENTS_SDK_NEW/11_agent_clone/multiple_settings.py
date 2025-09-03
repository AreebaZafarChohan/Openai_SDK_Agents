from config import config
from agents import Agent, ModelSettings, Runner


base_agent = Agent(
    name="BaseAssistant",
    instructions="You are a helpful assistant.",
    model_settings=ModelSettings(temperature=0.7)
)

# simple clone

creative_agent = base_agent.clone(
    name="CreativeAssistant",
    instructions="You are a creative writing assistant.",
    model_settings=ModelSettings(temperature=0.9)
)

precise_agent = base_agent.clone(
    name="PreciseAgent",
    instructions="You are a very precise and detail-oriented assistant.",
    model_settings=ModelSettings(temperature=0.1)
)

query = "Describe a sunset in short."

result_creative = Runner.run_sync(creative_agent, query, run_config=config)
result_precise = Runner.run_sync(precise_agent, query, run_config=config)


print("\nCreative Agent:", result_creative.final_output)
print("\n", "==="*50)
print("\nPrecise Agent:", result_precise.final_output)