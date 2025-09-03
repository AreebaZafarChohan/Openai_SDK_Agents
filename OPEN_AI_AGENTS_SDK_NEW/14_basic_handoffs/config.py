import os
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
from openai import AsyncOpenAI

load_dotenv()

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
BASE_URL= "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url=BASE_URL,
)

model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config: RunConfig = RunConfig(
    model=model,
    model_provider=external_client, # type: ignore
)