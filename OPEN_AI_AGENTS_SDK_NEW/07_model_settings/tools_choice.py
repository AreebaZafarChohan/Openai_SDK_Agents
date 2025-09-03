from agents import Agent, ModelSettings, Runner, function_tool, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

@function_tool
def add(a: int, b: int) -> int:
    "add two numbers"
    return a + b

@function_tool
def get_weather(city: str) -> str:
    "Fetch weather of given city or location and return it"
    return f"The weather of {city} is rainny."
    

auto_agent = Agent(
    name="Smart Agent",
    instructions="You are a smart and helping assistant",
    tools=[add, get_weather],
    model_settings=ModelSettings(tool_choice="auto")
)

required_agent = Agent(
    name="Tool User Agent",
    instructions="You are a smart and helping assistant always use tools.",
    tools=[add, get_weather],
    model_settings=ModelSettings(tool_choice="required")
)

no_tools_agent = Agent(
    name="Chat Only Agent",
    instructions="You are a smart and helping assistant. Never use tools",
    tools=[add, get_weather],
    model_settings=ModelSettings(tool_choice="none"),
)

prompt: str = """
    1. What is 9 + 2?
    2. Tell me about today's weather of karachi.
    3. What is openai sdk agent tell me in short.

"""

print("Tool Choice : 'auto' ")
auto_tools_result = Runner.run_sync(auto_agent, prompt, run_config=config)
print(auto_tools_result.final_output)
print("\n","="*70, "\n")

print("Tool Choice : 'required' ")
required_tools_result = Runner.run_sync(required_agent, prompt, run_config=config)
print(required_tools_result.final_output)

print("\n","="*70, "\n")


print("Tool Choice : 'none' ")
none_tools_result = Runner.run_sync(no_tools_agent, prompt, run_config=config)
print(none_tools_result.final_output)

print("\n","="*70, "\n")
