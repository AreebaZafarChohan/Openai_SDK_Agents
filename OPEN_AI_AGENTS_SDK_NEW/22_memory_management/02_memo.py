import os
from dotenv import load_dotenv
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner, function_tool
from openai import AsyncOpenAI
from mem0 import MemoryClient
import asyncio
import warnings

# Ignore asyncio + deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set default event loop policy (Windows fix)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
BASE_URL= "https://generativelanguage.googleapis.com/v1beta/openai/"
MEMO_API_KEY= os.getenv("MEMO_API_KEY")

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

mem0 = MemoryClient(api_key=MEMO_API_KEY)

@function_tool
def add_memory(query: str, user_id: str) -> str:
    """Add a memory to the memory system."""
    return str(mem0.add(
       [{
           "role": "user", "content": query
       }], user_id=user_id
    ))

@function_tool
def search_memory(query: str, user_id: str) -> str:
    """Search for relevant memories."""
    return str(mem0.search(query, user_id=user_id, limit=3))  

agent = Agent(
    name="Memory Assistant",
    instructions="""You are a hepful assistant with memory.
    Always check memory first before answering.
    Save new details about the user whenever possible.""",
    tools=[search_memory, add_memory],
    
)

USER_ID = "areeba_123"  # fixed user id

while True:
    input_text = input("\n [User:] ")
    if input_text.lower() in ["exit", "quit"]:
        break

    # input ko role+content ke sath bhejna (agent samjhega ke yeh ek user msg hai)
    res = Runner.run_sync(
        agent,
        [{"role": "user", "content": input_text}, {"role": "user", "content": f"user_id={USER_ID}"}],
        run_config=config,
    )

    print("\n [AGENT:]", res.final_output)

