from venv import logger
from agents import Agent, ModelSettings, Runner, enable_verbose_stdout_logging, function_tool
import rich
from config import config

# enable_verbose_stdout_logging()

@function_tool
def division(a: int, b: int) -> str:
    try:
        result = a / b
        return str(result)
    except ZeroDivisionError:
        return "Error: You cannot divide by zero. Please ask for a different number."
    # return str(a/b)
    

def my_failure_handler(exception, context, args=None):
    logger.error(f"Error occurred: {exception}, Context: {context}, Args: {args}")
    return f"An error occurred while processing your request. Tool Error: {exception}"

@function_tool(failure_error_function=my_failure_handler) # type: ignore
def raise_error_func() -> str:
    raise ValueError("This is a forced error.")

agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant. Always use tools.",
    tools=[division, raise_error_func],
    tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(tool_choice="required")
)

# result = Runner.run_sync(agent,
#                 """
#                 1. What is 10/0 ?
#                 2. Raise an error with raise_error_func
#                 """,
#                 run_config=config)
# print(result.final_output)
# # rich.print(result.new_items)


result = Runner.run_sync(
    agent,
    """
    What is 10/0? Use `division` tool
    """,
    run_config=config
)
print("Result 1:", result.final_output)
# rich.print(f"New Items 1: \n{result.new_items}")

result2 = Runner.run_sync(
    agent,
    """
    Raise an error with raise_error_func
    """,
    run_config=config
)
print("Result 2:", result2.final_output)
# rich.print(f"New Items 2: {result2.new_items}")
