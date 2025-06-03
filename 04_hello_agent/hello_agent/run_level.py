import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner # type: ignore
from agents.run import RunConfig # type: ignore

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Yaram Kazmi", instructions="You are a helpful assistant and always appriciate on good things or user or motivate him/her. Your owner is Areeba Zafar and your name is Yaram Kazmi")

result = Runner.run_sync(agent, "Hello, how are you tell me your name your owner and tell me about Pakistan and Karachi", run_config=config) # type: ignore

print(result.final_output)
