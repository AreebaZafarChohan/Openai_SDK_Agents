from typing import Any
from agents import Agent, ModelResponse, RunContextWrapper, AgentHooks, RunResult, Runner, function_tool
from config import config

class CustomAgentHooks(AgentHooks):    
    async def on_start(self, context: RunContextWrapper[Any], agent: Agent[Any]) -> None:
        print(f"\nAgent Start with : {agent.name} | Context: {context}")
        
    async def on_llm_start(self, context: RunContextWrapper[Any], agent: Agent[Any], system_prompt: str | None, input_items) -> None:
        print(f"\nLLM Start with: {agent.name} | {system_prompt} | {input_items}")
    
    async def on_llm_end(self, context: RunContextWrapper[Any], agent: Agent[Any], response: ModelResponse) -> None:
        print(f"\nLLM End with: {agent.name} | {response}")
    
    async def on_tool_start(self, context: RunContextWrapper[Any], agent: Agent[Any], tool) -> None:
        print(f"\nTool Start with: {agent.name} | {tool}")
    
    async def on_tool_end(self, context: RunContextWrapper[Any], agent: Agent[Any], tool, result: str) -> None:
        print(f"\nTool End with: {agent.name} | {tool} | {result}")
        
    async def on_handoff(self, context: RunContextWrapper[Any], agent: Agent[Any], source: Agent[Any]) -> None:
        print(f"\nHandoff: from {source.name} to {agent.name}")
    
    async def on_end(self, context: RunContextWrapper[Any], agent: Agent[Any], output: Any) -> None:
        print(f"\nAgent End with: {agent.name} | {output}")
        
custom_agent_hooks = CustomAgentHooks()
        
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
    hooks=custom_agent_hooks,

)    

res = Runner.run_sync(
    general_agent,
    """
    1. What is 10 * 2?
    2. Tell me todya's weather of karachi. 
    3. What is AI tell me in short.
    """,
    run_config=config
)

print("\n\n")
print(res.final_output)
print(res.last_agent.name)