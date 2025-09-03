import os
from agents import OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
from openai import AsyncOpenAI

# load env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

print(f"Loaded GEMINI API Key: {gemini_api_key is not None}")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)
config = RunConfig(
    model=model,
    model_provider=external_client, # type: ignore
    tracing_disabled=True
)