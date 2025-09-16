from config import config
from agents import Agent, Runner, enable_verbose_stdout_logging, function_tool, handoff, ModelSettings , StopAtTools
from agents.lifecycle import AgentHooksBase, RunHooksBase
from typing import Any
import time
import asyncio
from datetime import datetime

# enable_verbose_stdout_logging()

class DetailedAgentHooks(AgentHooksBase[Any, Agent[Any]]):
    def __init__(self):
        self.start_time = None
        self.llm_calls = 0
        self.tool_calls = 0
    
    async def on_start(self, context, agent):
        self.start_time = time.time()
        self.llm_calls = 0
        self.tool_calls = 0
        timestamp = datetime.now().strftime("%H:%M:%S")
        print("\n\nAgent Hook:")
        print(f"🕘 [{timestamp}] {agent.name} became active")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        self.llm_calls += 1
        print("\n\nAgent Hook:")
        print(f"📞 LLM Call #{self.llm_calls}: {agent.name} asking AI for guidance")
        print(f"   Input: {len(input_items)} items to think about")
    
    async def on_llm_end(self, context, agent, response):
        print("\n\nAgent Hook:")
        print(f"🧠✨ LLM Call #{self.llm_calls} completed")
        print(f"   AI response length: {len(str(response))} characters")
    
    async def on_tool_start(self, context, agent, tool):
        self.tool_calls += 1
        print("\n\nAgent Hook:")
        print(f"🔨 Tool #{self.tool_calls}: {agent.name} using {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print("\n\nAgent Hook:")
        print(f"✅🔨 Tool #{self.tool_calls} completed")
        print(f"   Result preview: {str(result)[:50]}...")
    
    async def on_handoff(self, context, agent, source):
        print("\n\nAgent Hook:")
        print(f"🏃‍♂️➡️🏃‍♀️ {agent.name} received work from {source.name}")
        print(f"   Work is being transferred due to specialization")
    
    async def on_end(self, context, agent, output):
        duration = time.time() - self.start_time if self.start_time else 0
        print("\n\nAgent Hook:")
        print(f"✅ {agent.name} FINISHED in {duration:.2f} seconds")
        print(f"📊 Total: {self.llm_calls} AI calls, {self.tool_calls} tool uses")
        print(f"🎯 Final result: {str(output)[:100]}...")
        
class DetailedRunHooks(RunHooksBase[Any, Agent[Any]]):
    def __init__(self):
        self.start_time = None
        self.llm_calls = 0
        self.tool_calls = 0
    
    async def on_agent_start(self, context, agent):
        self.start_time = time.time()
        self.llm_calls = 0
        self.tool_calls = 0
        timestamp = datetime.now().strftime("%H:%M:%S")
        print("\n\nRun Hook:")
        print(f"🕘 [{timestamp}] {agent.name} became active")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        self.llm_calls += 1
        print("\n\nRun Hook:")
        print(f"📞 LLM Call #{self.llm_calls}: {agent.name} asking AI for guidance")
        print(f"   Input: {len(input_items)} items to think about")
    
    async def on_llm_end(self, context, agent, response):
        print("\n\nRun Hook:")
        print(f"🧠✨ LLM Call #{self.llm_calls} completed")
        print(f"   AI response length: {len(str(response))} characters")
    
    async def on_tool_start(self, context, agent, tool):
        self.tool_calls += 1
        print("\n\nRun Hook:")
        print(f"🔨 Tool #{self.tool_calls}: {agent.name} using {tool.name}")
    
    async def on_tool_end(self, context, agent, tool, result):
        print("\n\nRun Hook:")
        print(f"✅🔨 Tool #{self.tool_calls} completed")
        print(f"   Result preview: {str(result)[:50]}...")
    
    async def on_handoff(self, context, from_agent, to_agent):
        print("\n\nRun Hook:")
        print(f"🏃‍♂️➡️🏃‍♀️ {from_agent.name} received work from {to_agent.name}")
        print(f"   Work is being transferred due to specialization")
    
    async def on_agent_end(self, context, agent, output):
        duration = time.time() - self.start_time if self.start_time else 0
        print("\n\nRun Hook:")
        print(f"✅ {agent.name} FINISHED in {duration:.2f} seconds")
        print(f"📊 Total: {self.llm_calls} AI calls, {self.tool_calls} tool uses")
        print(f"🎯 Final result: {str(output)[:100]}...")        
        
@function_tool
async def reset_password() -> str:
    await asyncio.sleep(1)
    return f"Password reset link sent to user@example.com"


reset_password_agent = Agent(name="ResetPassword", instructions="Assist customers with password reset inquiries. call tool `reset_password`.", tools=[reset_password], handoff_description="Transfer user reset password query to `reset_password` tool.", model_settings=ModelSettings(tool_choice="required"), tool_use_behavior=StopAtTools(stop_at_tool_names=["reset_password"]))


# Use it with your agent
customer_service = Agent(name="CustomerService", instructions="Assist customers with their inquiries.", handoffs=[handoff(reset_password_agent, tool_name_override="reset_password_tool", tool_description_override="Tool for resetting user passwords")])
customer_service.hooks = DetailedAgentHooks()
reset_password_agent.hooks = DetailedAgentHooks()

result = Runner.run_sync(customer_service, "How do I reset my password?", run_config=config, hooks=DetailedRunHooks())
print(f"Final result: {result}")

