from config import config
from agents import Agent, RunContextWrapper, RunResult, Runner, enable_verbose_stdout_logging, handoff

enable_verbose_stdout_logging()

# default behind the scene handoff name as a tool "transfer_to_billing_agent"
# default description "Handoff to the Billing Agent agent to handle the request."

# billing_agent: Agent = Agent(
#     name="Billing Agent",
#     instructions="You are a billing agent."
# )

# triage_agent: Agent = Agent(
#     name="Triage Agent",
#     instructions="You are a triage agent. You will determine the nature of the customer's issue and hand off to the appropriate agent.",
#     handoffs=[billing_agent]
# )

# agar hum us agent me handoff description dete hain to wo default k sath add hokr ayega like this 
# "Handoff to the Billing Agent agent to handle the request. Handoff the user query to the Billing Agent to handle the request."

# billing_agent: Agent = Agent(
#     name="Billing Agent",
#     instructions="You are a billing agent.",
#     handoff_description="Handoff the user query to the Billing Agent to handle the request."   
# )   

# triage_agent: Agent = Agent(
#     name="Triage Agent",
#     instructions="You are a triage agent. You will determine the nature of the customer's issue and hand off to the appropriate agent.",
#     handoffs=[billing_agent],
#     # handoff_description="Handoff user query to appropriate agent who are specialists."
# )

# def on_handoff(ctx: RunContextWrapper):
#     # Custom logic to execute when handing off to the billing agent
#     print(f"\nHanding off to {billing_agent.name} with context: {ctx.context}\n")

# billing_agent: Agent = Agent(
#     name="Billing Agent",
#     instructions="You are a billing agent.",
#     handoff_description="Handoff the user query to the Billing Agent to handle the request."   
# )   


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def log_handoff_event(ctx: RunContextWrapper):
    print(f"HANDOFF INITIATED: Transferring to the Escalation Agent at {ctx.context}")

specialist = Agent(name="Escalation Agent")
custom_handoff = handoff(
    agent=specialist,
    tool_name_override="escalate_to_specialist",
    tool_description_override="Use this for complex issues that require a specialist.",
    on_handoff=log_handoff_event,
)

triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions="You are a triage agent. You will determine the nature of the customer's issue and hand off to the appropriate agent.",
    # handoffs=[handoff(
    #     billing_agent,
    #     tool_name_override="billing_agent",  # tool name me kabhi bhi space nh ayegaa
    #     tool_description_override="Handoff the user query to the Billing Agent to handle the request.",
    #     on_handoff=on_handoff
    #     ), custom_handoff],
    
    handoffs=[custom_handoff]
)

query1 = "I want to bill my order. Order_id: 12345, Amount: 100 USD and escalate to specialist"
query2 = "I have a technical issue with my account."

result: RunResult = Runner().run_sync(triage_agent, query2, run_config=config)

print(result.final_output)
print(result.last_agent)


