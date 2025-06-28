import asyncio
import os
from random import randint
from dotenv import load_dotenv
from agents import Agent, ItemHelpers, OpenAIChatCompletionsModel, Runner, function_tool 
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

# Agents as tool

spanish_agent = Agent(
    name="spanish_agent",
    instructions="You translate the user's message to Spanish",
    handoff_description="An english to spanish translator",
    model=model
)

french_agent = Agent(
    name="french_agent",
    instructions="You translate the user's message to French",
    handoff_description="An english to french translator",
    model=model
)

italian_agent = Agent(
    name="italian_agent",
    instructions="You translate the user's message to Italian",
    handoff_description="An english to italian translator",
    model=model
)

pathan_agent = Agent(
    name="pathan_agent",
    instructions="You translate the user's message to pathani language of pakistan",
    handoff_description="An english to pathani translator",
    model=model
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate."
        "If asked for multiple translations, you call the relevant tools in order."
        "You never translate on your own, you always use the provided tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message into spanish.",
        ),
        
        italian_agent.as_tool(
            tool_name="translate_to_italian",
            tool_description="Translate the user's message into italian."
        ),
        
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message into french."
        ),
        
        pathan_agent.as_tool(
            tool_name="translate_to_pathani",
            tool_description="Translate the user's message into pathani."
        ),
    ],
    model=model
)
    
async def main():
    msg = input("Hi! What would you like translated, and to which languages?")
    
    orchestrator_result = await Runner.run(orchestrator_agent, input=msg, run_config=config)
    print(f"\n\nFinal response:\n{orchestrator_result.final_output}")

if __name__ == "__main__":
    asyncio.run(main())