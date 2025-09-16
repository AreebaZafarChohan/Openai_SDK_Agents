from pydantic import BaseModel
from config import config
from agents import Agent, RunContextWrapper, RunResult, Runner, enable_verbose_stdout_logging, handoff

enable_verbose_stdout_logging()

# class EscalationData(BaseModel):
#     reason: str
#     order_id: str

# def on_escalation(ctx: RunContextWrapper, input_data: EscalationData) -> None:
#     print(f"Escalating order {input_data.order_id} | {ctx.context.order_id} | {ctx.context.reason} | because: {input_data.reason}")
 
# specialist = Agent(name="Escalation Agent")
# custom_handoff = handoff(
#     agent=specialist,
#     tool_name_override="escalate_to_specialist",
#     tool_description_override="Use this for complex issues that require a specialist.",
#     on_handoff=on_escalation,
#     input_type=EscalationData
# )

# triage_agent: Agent = Agent(
#     name="Triage Agent",
#     instructions=(
#         "You are a triage agent. Always decide whether to solve directly or escalate. "
#         "If user mentions specialist or complex issue, call `escalate_to_specialist` with reason and order_id."
#     ),
#     # handoffs=[handoff(
#     #     billing_agent,
#     #     tool_name_override="billing_agent",  # tool name me kabhi bhi space nh ayegaa
#     #     tool_description_override="Handoff the user query to the Billing Agent to handle the request.",
#     #     on_handoff=on_handoff
#     #     ), custom_handoff],
    
#     handoffs=[custom_handoff]
# )

class UserBillingData(BaseModel):
    order_id: str
    amount: str
    reason: str

def on_handoff(ctx: RunContextWrapper, input_data: UserBillingData):
    # Custom logic to execute when handing off to the billing agent
    print(f"\nHanding off to {billing_agent.name} with user billing data. Order ID: {ctx.context.order_id}, Amount: {ctx.context.amount}, Reason: {ctx.context.reason}\n")

billing_agent: Agent = Agent(
    name="Billing Agent",
    instructions="You are a billing agent.",
    handoff_description="Handoff the user query to the Billing Agent to handle the request."   
)  

custom_handoff = handoff(
    billing_agent,
    tool_name_override="billing_agent",
    tool_description_override="Handoff the user query to the Billing Agent to handle the request.",
    on_handoff=on_handoff,
    input_type=UserBillingData,
    
)

triage_agent: Agent = Agent(
    name="Triage Agent",
    instructions=(
       "You are a triage agent. "
        "If the user query is about billing, you MUST call the `billing_agent` tool "
        "with fields: order_id, amount, reason. "
        "Do not answer directly."
    ),
    handoffs=[custom_handoff]
)

user_billing_data: UserBillingData = UserBillingData(order_id="12345", amount="500 USD", reason="Billing Order")

query1 = "I want to bill my order. Order ID: 12345, Amount: 500 USD, Reason: Billing Order"
query2 = "I have a technical issue with my account."

# escalation_data: EscalationData = EscalationData(order_id="12345", reason="I have a technical issue with my account.")

# result: RunResult = Runner().run_sync(triage_agent, query2, run_config=config , context=escalation_data)
result: RunResult = Runner().run_sync(triage_agent, query1, run_config=config, context=user_billing_data)

print(result.final_output)
print(result.last_agent)
