import asyncio
from pdb import run
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from config import config

# Define what our guardrail should output
class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

# Create a simple, fast agent to do the checking
guardrail_agent = Agent( 
    name="Homework Police",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)

# Create our guardrail function
@input_guardrail
async def math_guardrail( 
    ctx: RunContextWrapper[None], 
    agent: Agent, 
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    # Run our checking agent
    result = await Runner.run(guardrail_agent, input, context=ctx.context, run_config=config)
    
    # Return the result with tripwire status
    return GuardrailFunctionOutput(
        output_info=result.final_output, 
        tripwire_triggered=result.final_output.is_math_homework,  # Trigger if homework detected
    )

# Main agent with guardrail attached
customer_support_agent = Agent(  
    name="Customer Support Specialist",
    instructions="You are a helpful customer support agent for our software company.",
    input_guardrails=[math_guardrail],  # Attach our guardrail
)

# Testing the guardrail
async def test_homework_detection():
    try:
        # This should trigger the guardrail
        await Runner.run(customer_support_agent, "Can you solve 2x + 3 = 11 for x?", run_config=config)
        print("❌ Guardrail failed - homework request got through!")
    
    except InputGuardrailTripwireTriggered:
        print("✅ Success! Homework request was blocked.")
        # Handle appropriately - maybe send a polite rejection message
        
asyncio.run(test_homework_detection())        