from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from config import config        

enable_verbose_stdout_logging()

@function_tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers exactly."""
    return a - b

@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers exactly."""
    return a + b

agent: Agent = Agent(
    name="Assistant",  
    instructions="You are a helpful assistant. Always use tools for math questions and follow DMAS rule and explainclearly.",
    tools=[add, subtract],
)
result = Runner.run_sync(agent, "What is 5 - 10 + 15?", run_config=config)
print("\n🤖 CALLING AGENT\n")
print(result.final_output)
   