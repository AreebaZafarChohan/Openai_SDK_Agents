import asyncio
import os
from dotenv import load_dotenv
from agents import Agent, FileSearchTool, OpenAIChatCompletionsModel, Runner, WebSearchTool, function_tool 
from agents.run import RunConfig
from openai import AsyncOpenAI

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
    model_provider=external_client, # type: ignore
    tracing_disabled=True
)

# Function Tool
@function_tool()
def get_weather(location: str, unit: str = "C") -> str:
    """
    Fetch the weather for a given location and return it.
    """
    
    # Example logic
    return f"The weather in {location} is 22 degreees {unit}"

async def main():
    agent: Agent = Agent(name="Asssitant", instructions="You are a helping assistant and always use tools.", tools=[
        get_weather,
        # WebSearchTool(),
        # FileSearchTool(
        #     max_num_results=3,
        #     # vector_store_ids=["VECTOR_STORE_ID"]
        #     vector_store_ids=["vs_6813268d82a081919782a0990f3a68f9"],
        # ),   #  Hosted tools are not supported with the ChatCompletions API
    ],
)
    # query = "Show Muhammad Qasim current organization and job title"
    query = "Tell me today's weather of karachi."
    # query = "Current Pakistan India News"
    
    result = await Runner.run(agent, query, run_config=config)
    print(result.final_output)    

if __name__ == "__main__":
    asyncio.run(main())