from config import config
from agents import Agent, HandoffInputData, ModelSettings, RunContextWrapper, RunItem, RunResult, Runner, enable_verbose_stdout_logging, function_tool, handoff
from agents.extensions import handoff_filters
enable_verbose_stdout_logging()

@function_tool
def get_weather(location: str) -> str:
    return f"The weather in {location} is sunny."

@function_tool
def get_current_time(city: str) -> str:
    return f"The current time in {city} is 7:00 PM."

def on_handoff(ctx: RunContextWrapper):
    # Custom logic to execute when a handoff occurs
    print("\nHandoff occurred")
    print("Context:", ctx.context)
    
    
# def summarize_history_filter(handoff_input_data: HandoffInputData) -> HandoffInputData:
#     """
#     Custom filter: takes full conversation history and replace it with a single summarized message before handing off.
#     """
    
#     all_texts = []
    
#     for item in handoff_input_data.input_history:
#         if isinstance(item, RunItem) and hasattr(item,"content"):
#             all_texts.append(f"{item.role}: {item.content}") # type: ignore
#             print(f"Adding to summary: {item.role}: {item.content}") # type: ignore
        
#         elif isinstance(item, dict):
#             role = item.get("role","unknown")
#             content = item.get("content","")
#             all_texts.append(f"{role}: {content}")
#             print(f"Adding to summary: {role}: {content}")
    
#     history_text = "\n".join(all_texts)
#     print("\nFull conversation history to summarize:\n", history_text)
    
#     if len(history_text) > 300:
#         summary_text = history_text[:300] + " ... (truncated)"
#     else:
#         summary_text = history_text
        
#     summary_item = {"role": "system", "content": f"Conversation Summary:\n{summary_text}"}
#     print("\nSummary to send to the next agent:\n", summary_item)
     
#     return handoff_input_data.clone(
#         input_history=(summary_item,),
#         pre_handoff_items=handoff_input_data.pre_handoff_items,
#         new_items=handoff_input_data.new_items,
#         run_context=handoff_input_data.run_context
#     )
    

def add_system_context(handoff_input_data: HandoffInputData):
    # Add VIP system message as dict
    extra = {"role": "system", "content": "This is a VIP customer. Handle with care."}
    
    input_history = handoff_input_data.input_history
    
    # Ensure it's tuple of dicts
    if isinstance(input_history, str):
        input_history = ({"role": "user", "content": input_history},)
    elif not isinstance(input_history, tuple):
        input_history = tuple(input_history)
    
    # Prepend system context
    new_history = (extra,) + input_history
    print("Updated input history:", new_history)
    
    return handoff_input_data.clone(input_history=new_history)


billing_agent: Agent = Agent(
    name="Billing Agent",
    instructions="You are a billing agent.",
    handoff_description="Handoff the user query to the Billing Agent to handle the request."   
)  

history_teacher: Agent = Agent(
    name="History Teacher",
    instructions="You are a history teacher. Your work is to teach history and answer questions related to historical events.",
)


history_summary_agent: Agent = Agent(
    name="History Summary Agent",
    instructions="You are a history summary agent. Your work is to summarize all conversation history and return a specific summary.",
)

custom_handoff = handoff(
    billing_agent,
    tool_name_override="billing_agent",
    tool_description_override="Handoff the user query to the Billing Agent to handle the request.",
    # input_filter=handoff_filters.remove_all_tools
)

custom_history_handoff = handoff(
    history_summary_agent,
    tool_name_override="history_summary_agent",
    tool_description_override="Handoff the user query to the History Summary Agent to handle the request.",
    on_handoff=on_handoff,
    input_filter=add_system_context
)

custom_history_teacher_handoff = handoff(
    history_teacher,
    tool_name_override="history_teacher",
    tool_description_override="Handoff the user query to the History Teacher to handle the request.",
    input_filter=add_system_context
)

triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a triage agent. Your job is to analyze the user's query and take the correct action:\n\n"
        "- If the query is about **billing**, you MUST call the `billing_agent` tool "
        "with fields: order_id, amount, and reason. Do not answer directly.\n"
        "- If the query is about **history summary**, you MUST hand off to the `History Summary Agent`.\n"
        "- If the query is about **history teaching**, you MUST hand off to the `History Teacher`.\n"
        "- If the query is about **weather**, you MUST call the `get_weather` tool with the location.\n"
        "- If the query is about **current time**, you MUST call the `get_current_time` tool with the city.\n"
        "- For any other queries, politely explain that you cannot handle it."
    ),
    handoffs=[custom_handoff, custom_history_teacher_handoff],
    tools=[get_weather, get_current_time],
    # model_settings=ModelSettings(parallel_tool_calls=True)  # Error: 'Parallel tool calls are not supported.' handoff k sath bhi or srf tools me bhi 
)

query1 = """Tell me weather in New York.
            Also I want to bill my order.
            Order ID: 12345,
            Amount: 500 USD,
            Reason: Billing Order"""
            
queries = """
    What is the weather in Lahore?       
    What is the time in Karachi?         
    Can you summarize our conversation?  
"""         

query3 = """
    What is the weather in Lahore?
    What is the time in Karachi?     
    Can you tell me about the history of Lahore? 

"""


# result: RunResult = Runner().run_sync(triage_agent, query2, run_config=config , context=escalation_data)
# result: RunResult = Runner().run_sync(triage_agent, queries, run_config=config)
result: RunResult = Runner.run_sync(triage_agent, query3, run_config=config)

print(result.final_output)
print(result.last_agent)
