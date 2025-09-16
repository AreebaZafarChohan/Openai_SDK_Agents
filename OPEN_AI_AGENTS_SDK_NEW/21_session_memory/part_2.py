import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# 🌿 Load environment variables
load_dotenv(find_dotenv())

# 🔐 Setup Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url=BASE_URL)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=external_client)

# Temporary memory (lost when program ends)
temp_session = SQLiteSession("temp_conversation")

# Persistent memory (saved to file)
persistent_session = SQLiteSession("user_123", "conversations.db")

agent = Agent(name="Assistant", instructions="You are helpful.", model=model)

# Use temporary session
result1 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=temp_session
)

# Use persistent session
result2 = Runner.run_sync(
    agent,
    "Remember: my favorite color is blue",
    session=persistent_session
)

result_3 = Runner.run_sync(
    agent,
    "What is my favorite color?",
    session=temp_session
)

result_4 = Runner.run_sync(
    agent,
    "What is my favorite color?",
    session=persistent_session
)

print("Temporary session response:", result_3.final_output)  # Likely won't remember
print("Persistent session response:", result_4.final_output)  # Should remember "blue"

print("Both sessions now remember your favorite color!")
print("But only the persistent session will remember after restarting the program.")