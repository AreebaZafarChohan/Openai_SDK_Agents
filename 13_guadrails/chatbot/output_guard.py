from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, output_guardrail
from pydantic import BaseModel
from config import config

class MessageOutput(BaseModel):
    response: str
    
class MathOutput(BaseModel):
    is_math: bool
    reasoning: str
    

guardrail_agent: Agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)        

@output_guardrail
async def math_output_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    
    print(f"Output: Guardrail triggered", output)
    result = await Runner.run(
        agent,
        output.response,
        context=ctx.context,
        run_config=config
    )
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )
    
    
    