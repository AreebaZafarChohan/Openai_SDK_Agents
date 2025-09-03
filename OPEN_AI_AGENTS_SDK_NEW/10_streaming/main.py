import asyncio
from dataclasses import dataclass
from agents import Agent, OpenAIChatCompletionsModel, RunContextWrapper, RunResultStreaming, Runner, enable_verbose_stdout_logging, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent
from dotenv import load_dotenv, find_dotenv
import os
import rich

_: bool = load_dotenv(find_dotenv())

gemini_api_key: str | None = os.environ.get("GEMINI_API_KEY")

enable_verbose_stdout_logging()

external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client,
)

@dataclass
class UserContext:
    username: str
    email: str | None = None

@function_tool()
async def search(local_context: RunContextWrapper[UserContext], query: str) -> str:
    import time
    time.sleep(30)
    return "No results found."

def special_prompt(special_context: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> str:
    # print(f"\nUser: {special_context.context},\nAgent: {agent.name}\n")
    return f"You are a math expert. User: {special_context.context.username}, Agent: {agent.name}. Please assist with math-related queries."

math_agent: Agent = Agent(
        name="Genius",
        instructions=special_prompt,
        model=llm_model,
        # tools=[search],
    )
# [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

async def call_agent():
    
    user_context: UserContext = UserContext(username="Areeba Zafar")
    
    output : RunResultStreaming = Runner.run_streamed(
        starting_agent=math_agent,
        input="search for the best math tutor in my area",
        context=user_context,
    )
    
    print(output)
    
    print("\n","**"*50)
    async for event in output.stream_events():
        rich.print(event)

asyncio.run(call_agent())            