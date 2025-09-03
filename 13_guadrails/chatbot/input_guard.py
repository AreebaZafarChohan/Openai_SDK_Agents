from typing import List
from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, Runner, TResponseInputItem, input_guardrail
from config import config


class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str
    
guardrail_agent: Agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeWorkOutput,
)    

@input_guardrail
async def math_input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | List[TResponseInputItem]
    ) -> GuardrailFunctionOutput:
    
    print(f"Input: Guardrail triggered", input)

    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=config,
    )
    
    return GuardrailFunctionOutput(
        output_info= result.final_output,
        tripwire_triggered= result.final_output.is_math_homework,
    )