from attr import dataclass
from config import config
from agents import Agent, RunContextWrapper, RunResult, Runner, enable_verbose_stdout_logging, handoff

# enable_verbose_stdout_logging()

@dataclass
class Student:
    student_id: str
    name: str
    age: int
    
    

billing_agent: Agent = Agent(
    name="Billing Agent",
    instructions="You are a billing agent.",
    handoff_description="Handoff the user query to the Billing Agent to handle the request."   
)  

history_teacher: Agent = Agent(
    name="History Teacher",
    instructions="You are a history teacher. Your work is to teach history and answer questions related to historical events.",
)

custom_billing_handoff = handoff(
    billing_agent,
    is_enabled=False,
)

def is_history_student(ctx: RunContextWrapper[Student], agent: Agent[Student]) -> bool:
    if ctx.context is None:
        return False
    return ctx.context.student_id.startswith("history")

custom_history_handoff = handoff(
    history_teacher,
    tool_name_override="history_teacher",
    tool_description_override="Handoff the user query to the History Teacher to handle the request.",
    is_enabled=is_history_student,
)


triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a triage agent. Your job is to analyze the user's query and take the correct action:\n\n"
        "- If the query is about **billing**, you MUST call the `billing_agent` tool "
        "with fields: order_id, amount, and reason. Do not answer directly.\n"
        "- If the query is about **history teaching**, you MUST hand off to the `History Teacher`.\n"
        "- For any other queries, politely explain that you cannot handle it."
        ),
    handoffs=[custom_billing_handoff, custom_history_handoff],
)

student_data: Student = Student(student_id="history_001", name="Alice", age=20)
student_data2: Student = Student(student_id="english_002", name="Bob", age=22)

query1 = "I want to bill my order. Order_id: 12345, Amount: 100 USD and escalate to specialist"
query2 = "Tell me about the history of Pakistan in two lines."

result1: RunResult = Runner().run_sync(triage_agent, query1, run_config=config)

result2: RunResult = Runner().run_sync(triage_agent, query2, run_config=config, context=student_data)
result3: RunResult = Runner().run_sync(triage_agent, query2, run_config=config, context=student_data2)

print("\n","*"*70, "\n")

print(result1.final_output)
print(result1.last_agent.name)

print("\n","*"*70, "\n")

print(result2.final_output)
print(result2.last_agent.name)

print("\n","*"*70, "\n")

print(result3.final_output)
print(result3.last_agent.name)

print("\n","*"*70, "\n")
