from typing import Any
from agents import Agent, ModelResponse, RunContextWrapper, RunHooks, RunResult, Runner, function_tool
from config import config

class CustomRunHooks(RunHooks):    
    async def on_agent_start(self, context: RunContextWrapper[Any], agent: Agent[Any]) -> None:
        print(f"\nAgent Start with : {agent.name} | Context: {context}")
            
    async def on_llm_start(self, context: RunContextWrapper[Any], agent: Agent[Any], system_prompt: str | None, input_items) -> None:
        print(f"\nLLM Start with: {agent.name} | {system_prompt} | {input_items}")
    
    async def on_llm_end(self, context: RunContextWrapper[Any], agent: Agent[Any], response: ModelResponse) -> None:
        print(f"\nLLM End with: {agent.name} | {response}")
    
    async def on_tool_start(self, context: RunContextWrapper[Any], agent: Agent[Any], tool) -> None:
        print(f"\nTool Start with: {agent.name} | {tool}")
    
    async def on_tool_end(self, context: RunContextWrapper[Any], agent: Agent[Any], tool, result: str) -> None:
        print(f"\nTool End with: {agent.name} | {tool} | {result}")
        
    async def on_handoff(self, context: RunContextWrapper[Any], from_agent: Agent[Any], to_agent: Agent[Any]) -> None:
        print(f"\nHandoff: from {from_agent.name} to {to_agent.name}")
                    
    async def on_agent_end(self, context: RunContextWrapper[Any], agent: Agent[Any], output: Any) -> None:
        print(f"\nAgent End with: {agent.name} | {output}")
        
custom_run_hooks = CustomRunHooks()
        
@function_tool
async def get_weather(city: str) -> str:
    return f"Weather of {city} is rainny."        

math_teacher = Agent(name="Math Agent", instructions="You are a Mathematics Specialist.")

general_agent = Agent(
    name="General Agent",
    instructions=(
    "You are a general agent answer user's query properly."
    "If user's query is about weather call `get_weather` tool."
    "If user's query is about mathematics related questions handoff to `math_teacher` agent."
), 
    tools=[get_weather],
    handoffs=[math_teacher],
)    

res = Runner.run_sync(
    general_agent,
    """
    1. What is 10 * 2?
    2. Tell me todya's weather of karachi. 
    3. What is AI tell me in short.
    """,
    run_config=config,
    hooks=custom_run_hooks,
)

print("\n\n")
print(res.final_output)
print(res.last_agent.name)



# import asyncio
# import os
# from typing import Any
# from agents import Agent, RunContextWrapper, AgentHooks, Runner, enable_verbose_stdout_logging
# from config import config

# enable_verbose_stdout_logging()

# start_agent = Agent(
#     name="Content Moderator Agent",
#     instructions="You are content moderation agent. Watch social media content received and flag queries that need help or answer. We will answer anything about AI?",
# )

# async def main():
#   result = await Runner.run(
#       start_agent,
#       input=f"Will Agentic AI Die at end of 2025?.",
#       run_config=config,
#   )

#   print(result.final_output)
  
# asyncio.run(main())  


# import asyncio
# from agents import Agent, ModelSettings, Runner, enable_verbose_stdout_logging, function_tool, tool

# enable_verbose_stdout_logging()

# # --- Define Tools ---
# @function_tool
# def weather_tool(location: str) -> str:
#     """Get weather info for a location"""
#     return f"Weather in {location} is Sunny 25°C"

# @function_tool
# def news_tool(topic: str) -> str:
#     """Get latest news on a topic"""
#     return f"Latest news on {topic}: AI adoption is booming"

# @function_tool
# def stock_tool(company: str) -> str:
#     """Get stock price of a company"""
#     return f"Stock price of {company}: $123.45"


# # --- Define Agents ---

# agent_weather = Agent(
#     name="Weather Agent",
#     instructions="You answer weather queries using the weather_tool.",
#     tools=[weather_tool],
# )

# agent_news = Agent(
#     name="News Agent",
#     instructions="You answer news queries using the news_tool.",
#     tools=[news_tool],
# )

# agent_stock = Agent(
#     name="Stock Agent",
#     instructions="You answer stock queries using the stock_tool.",
#     tools=[stock_tool],
# )


# triage_agent = Agent(
#     name="Triage Agent",
#     instructions=(
#         "You are a smart router agent. "
#         "Analyze the user request and decide whether to send it to the Weather Agent, "
#         "News Agent, or Stock Agent. "
#         "Split queries if multiple intents exist and hand them off in parallel."
#     ),
#     # handoffs=[agent_weather, agent_news, agent_stock],
#     # model_settings=ModelSettings(parallel_tool_calls=True)
# )

# # --- Main ---
# async def main():
#     result = await Runner.run(
#         agent_weather,
#         input="Tell me weather in Paris, news about AI, and stock price of Google.", 
#         run_config=config,
#         max_turns=20
#     )

#     print("\n=== Final Output ===")
#     print(result.final_output)


# asyncio.run(main())


