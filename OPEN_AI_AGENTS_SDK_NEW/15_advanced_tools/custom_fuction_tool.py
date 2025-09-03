import json
from venv import logger
from agents import Agent, FunctionTool, ModelSettings, Runner, enable_verbose_stdout_logging, function_tool
import rich
from config import config

# enable_verbose_stdout_logging()

# class CounterTool(FunctionTool):
#     def __init__(self):
#         self._count = 0
#         super().__init__(
#             name="incrementing_counter",
#             description="Counts up by one each time it is called.",
#             params_json_schema={"type": "object", "properties": {}},
#             on_invoke_tool=self.on_invoke_tool
#         )
    
#     async def on_invoke_tool(self, context, args_json_str) -> str: # type: ignore
#         self._count += 1
#         return f"The current count is {self._count}"

# counter_tool = CounterTool()


class MathCalculator(FunctionTool):
    def __init__(self):
        super().__init__(
            name="math_calculator",
            description="Performs basic math operations.",
            params_json_schema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to evaluate."
                    },
                },
                "required": ["expression"],
            },
            on_invoke_tool=self.on_invoke_tool
        )
        
    async def on_invoke_tool(self, context, args_json_str) -> str: # type: ignore
        args = json.loads(args_json_str)    
        expr = args.get("expression")
        try:
            if not all(c in "0123456789+-*/()." for c in expr):
                return "Erorr: Unsafe expression"
            return str(eval(expr))
        except Exception as e:
            return f"Error: {str(e)}"
        
math_calculator_tool = MathCalculator()        

agent: Agent = Agent(
    name="Agent",
    instructions="You are a helpful assistant. Always use tools.",
    tools=[math_calculator_tool],
    # tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(tool_choice="required")
)

result1 = Runner.run_sync(agent, "Hii Dear answer my greeting! What is 82*2?", run_config=config)
print("Result 1:", result1.final_output)

result2 = Runner.run_sync(agent, "Assalam o alikum buddy answer my greeting!! What is 5+3?", run_config=config)
print("Result 2:", result2.final_output)

result3 = Runner.run_sync(agent, "Hello Dude answer my greeting!! What is 10-4/35?", run_config=config)
print("Result 3:", result3.final_output)



# class TodoListTool(FunctionTool):
#     def __init__(self):
#         self.todos = []
#         super().__init__(
#             name="todo_manager",
#             description="Add, list, and remove tasks from a to-do list.",
#             params_json_schema={
#                 "type": "object",
#                 "properties": {
#                     "action": {"type": "string", "enum": ["add", "list", "remove"]},
#                     "task": {"type": "string"}
#                 },
#                 "required": ["action"]
#             },
#             on_invoke_tool=self.on_invoke_tool
#         )

#     async def on_invoke_tool(self, context, args_json_str: str) -> str:
#         args = json.loads(args_json_str)
#         action = args["action"]

#         if action == "add":
#             task = args.get("task", "")
#             self.todos.append(task)
#             return f"Task added: {task}"
#         elif action == "list":
#             return f"Tasks: {', '.join(self.todos) if self.todos else 'No tasks'}"
#         elif action == "remove":
#             task = args.get("task", "")
#             if task in self.todos:
#                 self.todos.remove(task)
#                 return f"Task removed: {task}"
#             return "Task not found"



# import random

# class JokeTool(FunctionTool):
#     def __init__(self):
#         super().__init__(
#             name="joke_generator",
#             description="Returns a random joke.",
#             params_json_schema={"type": "object", "properties": {}},
#             on_invoke_tool=self.on_invoke_tool
#         )

#     async def on_invoke_tool(self, context, args_json_str: str) -> str:
#         jokes = [
#             "Why don’t programmers like nature? It has too many bugs.",
#             "Why did the function break up with the loop? It felt too repetitive.",
#             "Debugging: Being the detective in a crime movie where you are also the murderer."
#         ]
#         return random.choice(jokes)
