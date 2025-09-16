from unittest import result
from config import config 
from agents import Agent, Runner, SQLiteSession


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be friendly and remember our conversation.",
)

session = SQLiteSession("my_first_conversation")

print("\n=== First Coversation with Memory ===\n")

result1 = Runner.run_sync(
    agent,
    "Assalam o alikum! I am Areeba Zafar and I love biryani.",
    session=session,
    run_config=config,
)

print("Agent:", result1.final_output)

result2 = Runner.run_sync(
    agent,
    "What food do I like?",
    session=session,
    run_config=config,
)

print("Agent:", result2.final_output)

result3 = Runner.run_sync(
    agent,
    "What is my name?",
    session=session,
    run_config=config,
)

print("Agent:", result3.final_output)

print("\n\n No Session Memory \n\n")

result4 = Runner.run_sync(
    agent,
    "What is my name and what do I like?",
    run_config=config,
)

print("Agent:", result4.final_output)