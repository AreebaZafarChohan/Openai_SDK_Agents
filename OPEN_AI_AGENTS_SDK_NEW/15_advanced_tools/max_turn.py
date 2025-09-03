from agents import Agent, MaxTurnsExceeded, Runner, enable_verbose_stdout_logging, function_tool, StopAtTools
import rich
from config import config

enable_verbose_stdout_logging()

agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant.",
)

# "run_llm_again" Default behaviour
try:
    res1 = Runner.run_sync(agent, "What's the full form of AI?", run_config=config, max_turns=0)
    print(res1.final_output)
    rich.print(res1.new_items)
except MaxTurnsExceeded as e:
    print(f"Max turns exceeded, as expected. Error: {str(e)} | {type(str(e))} - {e} | {type(e)} ")  


result = Runner.run_sync(agent, "Find articles about AI agents. You can think and act a maximum of 5 times.", max_turns=6, run_config=config)
print(result.final_output)