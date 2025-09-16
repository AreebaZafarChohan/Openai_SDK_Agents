import asyncio
from agents import Agent, Runner, SQLiteSession, enable_verbose_stdout_logging
from config import config
import asyncio

enable_verbose_stdout_logging()

    # Create agent
agent = Agent(
    name="Assistant",
    instructions="Reply very concisely.",
)
# Create a session instance with a session ID
session = SQLiteSession("conversation_123")
# First turn
result1 = Runner.run_sync(
    agent,
    "What city is the Golden Gate Bridge in?",
    session=session,
    run_config=config,
)
print(result1.final_output)  # "San Francisco"
# Second turn - agent automatically remembers previous context
result2 = Runner.run_sync(
    agent,
    "What state is it in?",
    session=session,
    run_config=config,
)
print(result2.final_output)  # "California"

# Also works with synchronous runner
result3 = Runner.run_sync(
    agent,
    "What's the population?",
    session=session,
    run_config=config,
)
print(result3.final_output)  # "Approximately 39 million"

