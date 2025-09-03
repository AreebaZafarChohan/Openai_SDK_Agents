from venv import logger
from agents import Agent, FunctionTool, ModelSettings, Runner, enable_verbose_stdout_logging, function_tool
import rich
from config import config

# enable_verbose_stdout_logging()

class CounterTool(FunctionTool):
    def __init__(self):
        self._count = 0
        super().__init__(
            name="incrementing_counter",
            description="Counts up by one each time it is called.",
            params_json_schema={"type": "object", "properties": {}},
            on_invoke_tool=self.on_invoke_tool
        )
    
    async def on_invoke_tool(self, context, args_json_str) -> str: # type: ignore
        self._count += 1
        return f"The current count is {self._count}"

counter_tool = CounterTool()

agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant. Always use tools.",
    tools=[counter_tool],
    # tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(tool_choice="required")
)

result1 = Runner.run_sync(agent, "Hii Dear answer my greeting! Increment the counter", run_config=config)
print("Result 1:", result1.final_output)

result2 = Runner.run_sync(agent, "Assalam o alikum buddy answer my greeting!! Increment the counter again", run_config=config)
print("Result 2:", result2.final_output)

result3 = Runner.run_sync(agent, "Hello Dude answer my greeting!! Increment one more time", run_config=config)
print("Result 3:", result3.final_output)
