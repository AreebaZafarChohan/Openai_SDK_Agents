import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool, RunContextWrapper
from agents.tool_context import ToolContext
from dataclasses import dataclass
from mem0 import MemoryClient
from openai import AsyncOpenAI
from config import config
import asyncio
import warnings

# Ignore asyncio + deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set default event loop policy (Windows fix)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@dataclass
class UserContext:
    username: str

_: bool = load_dotenv(find_dotenv())

set_tracing_disabled(True)

# ONLY FOR TRACING
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
MEMO_API_KEY= os.getenv("MEMO_API_KEY")


mem_client = MemoryClient(api_key=MEMO_API_KEY)

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
async def search_user_memory(context: ToolContext[UserContext], query: str):
    """Use this tool to search user memories."""
    response = mem_client.search(query=query, user_id=context.context.username, top_k=3)
    return response

@function_tool
async def save_user_memory(context: ToolContext[UserContext], query: str):
    """Use this tool to save user memories."""
    response = mem_client.add([{"role": "user", "content": query}], user_id=context.context.username)
    return response

def dynamic_instructions_generator(context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    return f"""
    You are a helpful assistant with memory. 
    - Always use search_user_memory to recall past details about the user.
    - Always use save_user_memory to remember new details the user tells you 
      (like their name, hobbies, favorites, etc.).
    - The user_id for memory is {context.context.username}.
    """


orchestrator_agent: Agent = Agent(
    name="DeepAgent",
    instructions=dynamic_instructions_generator,
    model=llm_model,
    tools=[save_user_memory, search_user_memory],
)

while True:
    # Part 1 Requirement Gathering
    input_text = input("\n [User:] ")
    if input_text.lower() in ["exit", "quit"]:
        break
    res = Runner.run_sync(orchestrator_agent, input_text, context=UserContext(username="muhammad"), run_config=config)
    print( "\n [AGENT:]" , res.final_output) # requirement_completed, question