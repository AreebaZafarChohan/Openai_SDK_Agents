from typing import Any
from config import config
from agents import Agent, AgentHooks, ModelResponse, RunContextWrapper, Runner, function_tool


class HelloAgentHooks(AgentHooks):
    def __init__(self, lifecycle_name: str) -> None:
        self.lifecycle_name = lifecycle_name
    
    async def on_start(self, context: RunContextWrapper[Any], agent: Agent[Any]) -> None:
        context.context
        print(f"\n\n[{self.lifecycle_name}] Agent {agent.name} starting with context {context}\n\n")
        
    async def on_llm_start(self, context: RunContextWrapper[Any], agent: Agent[Any], system_prompt: str | None, input_items) -> None:
        print(f"\n\n[{self.lifecycle_name}]LLM call starting with system prompt: {system_prompt} and input_items {input_items}\n\n")
    
    async def on_llm_end(self, context: RunContextWrapper[Any], agent: Agent[Any], response: ModelResponse) -> None:
        print(f"\n\n[{self.lifecycle_name}] LLM call ended with output: {response}\n\n")
        
    async def on_tool_start(self, context: RunContextWrapper[Any], agent: Agent[Any], tool) -> None:
        print(f"\n\n[{self.lifecycle_name}] Tool call with tool name: {tool.name}\n\n") 
    
    async def on_tool_end(self, context: RunContextWrapper[Any], agent: Agent[Any], tool, result) -> None:
        print(f"\n\n[{self.lifecycle_name}] Tool call ended with tool name: {tool.name} and tool result: {result}\n\n")
    
    async def on_handoff(self, context: RunContextWrapper[Any], agent: Agent[Any], source: Agent[Any]) -> None:
        print(f"\n\n[{self.lifecycle_name}] Handoff from agent {source.name} to agent {agent.name}\n\n")

    async def on_end(self, context: RunContextWrapper[Any], agent: Agent[Any], output: ModelResponse) -> None:
        print(f"\n\n[{self.lifecycle_name}] Agent {agent.name} ended with output: {output}\n\n")
        
@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"The weather for {city} is sunny."



news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You are a helpful news assistant.",
    hooks=HelloAgentHooks("NewsAgentLifecycle")
)


base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. Talk about weather and let news_agent handle the news things",
    tools=[get_weather],
    hooks=HelloAgentHooks("WeatherAgentLifecycle"),
    handoffs=[news_agent]
)

res = Runner.run_sync(base_agent, "What's the latest news about Qwen Code - seems like it can give though time to claude code.", run_config=config)
print(res.last_agent.name)
print(res.final_output)        