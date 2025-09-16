from config import config
from agents import Agent, Runner, enable_verbose_stdout_logging
from agents.lifecycle import AgentHooksBase
from typing import Any

enable_verbose_stdout_logging()

# # Create a custom hook class for our agent
# class MyAgentHooks(AgentHooksBase):
#     async def on_start(self, context, agent):
#         print(f"🕘 {agent.name} is starting up!")
    
#     async def on_llm_start(self, context, agent, system_prompt, input_items):
#         print(f"📞 {agent.name} is asking AI for help")
    
#     async def on_llm_end(self, context, agent, response):
#         print(f"🧠✨ {agent.name} got AI response")
    
#     async def on_tool_start(self, context, agent, tool):
#         print(f"🔨 {agent.name} is using {tool.name}")
    
#     async def on_tool_end(self, context, agent, tool, result):
#         print(f"✅ {agent.name} finished using {tool.name}")
    
#     async def on_end(self, context, agent, output):
#         print(f"🎉 {agent.name} completed the task!")

# Create a custom hook class for our agent
class MyAgentHooks(AgentHooksBase[Any, Agent[Any]]):
    async def on_start(self, context, agent):
        print(f"🕘 {agent.name} is starting up!")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        print(f"📞 {agent.name} is asking AI for help")
    
    async def on_llm_end(self, context, agent, response):
        print(f"🧠✨ {agent.name} got AI response")
    
    async def on_tool_start(self, context, agent, tool):
        print(f"🔨 {agent.name} is using {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"✅ {agent.name} finished using {tool.name}")
    
    async def on_end(self, context, agent, output):
        print(f"🎉 {agent.name} completed the task!")

# Create an agent
my_agent = Agent(
    name="Helper Bot",
    instructions="You are a helpful assistant."
)

# Attach our hooks to this specific agent
my_agent.hooks = MyAgentHooks()


result = Runner.run_sync(my_agent, "What is 5 multiplied by 3?", run_config=config)

print(f"Final result: {result}")