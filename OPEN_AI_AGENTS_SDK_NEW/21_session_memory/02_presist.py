from unittest import result
from config import config 
from agents import Agent, Runner, SQLiteSession


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Be friendly and remember our conversation.",
)

temp_session = SQLiteSession("temp_conversation")

presistent_session = SQLiteSession("user_123", "my_conversation.db")


result1 = Runner.run_sync(
    agent,
    "Remember my favourite color is blue.",
    session=temp_session,
    run_config=config,
)


result2 = Runner.run_sync(
    agent,
    "Remember my favourite color is blue.",
    session=presistent_session,
    run_config=config,
)


result3 = Runner.run_sync(
    agent,
    "What is my favourite color?",
    session=temp_session,
    run_config=config,
)

print("Agent:", result3.final_output)


result4 = Runner.run_sync(
    agent,
    "What is my favourite color?",
    session=presistent_session,
    run_config=config,
)

print("Agent:", result4.final_output)