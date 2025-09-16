import time
from datetime import datetime
from agents import Agent, RunHooks, Runner, TContext, function_tool
from agents.lifecycle import RunHooksBase
from config import config


class MultiAgentAnalytics(RunHooksBase[TContext, Agent]):
    def __init__(self):
        self.start_time = None
        self.agent_stats = {}
        self.system_stats = {
            'total_llm_calls': 0,
            'total_tool_calls': 0,
            'total_handoffs': 0
        }
    
    def _init_agent_stats(self, agent_name):
        if agent_name not in self.agent_stats:
            self.agent_stats[agent_name] = {
                'start_time': None,
                'total_time': 0,
                'llm_calls': 0,
                'tool_calls': 0
            }
    
    async def on_agent_start(self, context, agent):
        if self.start_time is None:
            self.start_time = time.time()
        
        self._init_agent_stats(agent.name)
        self.agent_stats[agent.name]['start_time'] = time.time()
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"🌅 [{timestamp}] SYSTEM: {agent.name} started working")
    
    async def on_llm_start(self, context, agent, system_prompt, input_items):
        self._init_agent_stats(agent.name)
        self.agent_stats[agent.name]['llm_calls'] += 1
        self.system_stats['total_llm_calls'] += 1
        
        print(f"📞 SYSTEM: {agent.name} LLM call #{self.agent_stats[agent.name]['llm_calls']}")
    
    async def on_llm_end(self, context, agent, response):
        print(f"🧠✨ SYSTEM: {agent.name} got LLM response")
    
    async def on_tool_start(self, context, agent, tool):
        self._init_agent_stats(agent.name)
        self.agent_stats[agent.name]['tool_calls'] += 1
        self.system_stats['total_tool_calls'] += 1
        
        print(f"🔨 SYSTEM: {agent.name} tool call #{self.agent_stats[agent.name]['tool_calls']} ({tool.name})")
    
    async def on_tool_end(self, context, agent, tool, result):
        print(f"✅🔨 SYSTEM: {agent.name} finished {tool.name}")
        print(f"   Result length: {len(str(result))} characters")
    
    async def on_handoff(self, context, from_agent, to_agent):
        self.system_stats['total_handoffs'] += 1
        print(f"🏃‍♂️➡️🏃‍♀️ HANDOFF #{self.system_stats['total_handoffs']}: {from_agent.name} → {to_agent.name}")
    
    async def on_agent_end(self, context, agent, output):
        if agent.name in self.agent_stats and self.agent_stats[agent.name]['start_time']:
            duration = time.time() - self.agent_stats[agent.name]['start_time']
            self.agent_stats[agent.name]['total_time'] = duration
        
        print(f"✅ SYSTEM: {agent.name} finished")
        print(f"   Duration: {duration:.2f}s") # type: ignore
        print(f"   LLM calls: {self.agent_stats[agent.name]['llm_calls']}")
        print(f"   Tool calls: {self.agent_stats[agent.name]['tool_calls']}")
        
        # Print system summary
        total_time = time.time() - self.start_time if self.start_time else 0
        print(f"\n📊 SYSTEM STATS:")
        print(f"   Total runtime: {total_time:.2f}s")
        print(f"   Total LLM calls: {self.system_stats['total_llm_calls']}")
        print(f"   Total tool calls: {self.system_stats['total_tool_calls']}")
        print(f"   Total handoffs: {self.system_stats['total_handoffs']}")
        print(f"   Agents used: {list(self.agent_stats.keys())}")

        
# --- Define Tools ---
@function_tool
def weather_tool(location: str) -> str:
    """Get weather info for a location"""
    return f"Weather in {location} is Sunny 25°C"

@function_tool
def news_tool(topic: str) -> str:
    """Get latest news on a topic"""
    return f"Latest news on {topic}: AI adoption is booming"

@function_tool
def stock_tool(company: str) -> str:
    """Get stock price of a company"""
    return f"Stock price of {company}: $123.45"


# --- Define Agents ---

agent_weather = Agent(
    name="Weather Agent",
    instructions="You answer weather queries using the weather_tool.",
    tools=[weather_tool],
)

agent_news = Agent(
    name="News Agent",
    instructions="You answer news queries using the news_tool.",
    tools=[news_tool],
)

agent_stock = Agent(
    name="Stock Agent",
    instructions="You answer stock queries using the stock_tool.",
    tools=[stock_tool],
)


triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a smart router agent. "
        "Analyze the user request and decide whether to send it to the Weather Agent, "
        "News Agent, or Stock Agent. "
        "Split queries if multiple intents exist and hand them off in parallel."
    ),
    # handoffs=[agent_weather, agent_news, agent_stock],
    tools=[news_tool, stock_tool, weather_tool]
    # model_settings=ModelSettings(parallel_tool_calls=True)
)

result = Runner.run_sync(
    starting_agent=triage_agent,
    input="Tell me weather in Paris, news about AI, and stock price of Google.",
    hooks=MultiAgentAnalytics(),  # This monitors EVERYTHING
    run_config=config
)

print(result.final_output)        