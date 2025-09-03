from agents import Agent, ModelSettings, Runner, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

brief_agent: Agent = Agent(
    name="Brief Agent",
    instructions="You are a brief agent.",
    model_settings=ModelSettings(max_tokens=50)
)

detailed_agent: Agent = Agent(
    name="Detailed Agent",
    instructions="You are a detailed agent.",
    model_settings=ModelSettings(max_tokens=500)
)

prompt: str = "Tell me about Pakistan."

print("\n","="*70, "\n")

print("Max Tokens = 50 ")
brief_result = Runner.run_sync(brief_agent, prompt, run_config=config)
print(brief_result.final_output)

print("\n","="*70, "\n")


print("Max Tokens = 500 ")
detailed_result = Runner.run_sync(detailed_agent, prompt, run_config=config)
print(detailed_result.final_output)

print("\n","="*70, "\n")