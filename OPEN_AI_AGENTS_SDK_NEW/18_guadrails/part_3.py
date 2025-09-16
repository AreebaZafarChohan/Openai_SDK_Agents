import asyncio
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    enable_verbose_stdout_logging,
    output_guardrail,
)
from config import config

enable_verbose_stdout_logging()

class MessageOutput(BaseModel): 
    response: str

class SensitivityCheck(BaseModel): 
    contains_sensitive_info: bool
    reasoning: str
    confidence_level: int  # 1-10 scale

# Fast guardrail agent for checking outputs
sensitivity_guardrail_agent = Agent(
    name="Privacy Guardian",
    instructions="""
    Check if the response contains:
    - Personal information (SSN, addresses, phone numbers)
    - Internal company information
    - Confidential data
    - Inappropriate personal details
    
    Be thorough but not overly sensitive to normal business information.
    """,
    output_type=SensitivityCheck,
)

@output_guardrail
async def privacy_guardrail(  
    ctx: RunContextWrapper, 
    agent: Agent, 
    output: MessageOutput
) -> GuardrailFunctionOutput:
    # Check the agent's response for sensitive content
    result = await Runner.run(
        sensitivity_guardrail_agent, 
        f"Please analyze this customer service response: {output.response}", 
        context=ctx.context,
        run_config=config,
    )
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_sensitive_info,
    )

# Main customer support agent with output guardrail
support_agent = Agent( 
    name="Customer Support Agent",
    instructions="Help customers with their questions. Be friendly and informative.",
    output_guardrails=[privacy_guardrail],  # Add our privacy check
    output_type=MessageOutput,
)

async def test_privacy_protection():
    try:
        # This might generate a response with sensitive info
        result = await Runner.run(
            support_agent, 
            "What's my account status for john.doe@email.com?",
            run_config=config,
        )
        print(f"✅ Response approved: {result.final_output.response}")
    
    except OutputGuardrailTripwireTriggered as e:
        print("🛑 Response blocked - contained sensitive information!")
        # Send a generic response instead
        fallback_message = "I apologize, but I need to verify your identity before sharing account details."
        
asyncio.run(test_privacy_protection())        