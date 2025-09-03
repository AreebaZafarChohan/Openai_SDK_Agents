import asyncio
from typing import List
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)
from config import config

class MathHomeWorkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Cehck if the user is asking you to do their math homework.",
    output_type=MathHomeWorkOutput,
)    

@input_guardrail
async def math_gaurdrail(ctx: RunContextWrapper[None], agnet: Agent, input: str | List[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_agent,
        input,
        context=ctx.context,
        run_config=config,
    )
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= result.final_output.is_math_homework,
    )
    
agent: Agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_gaurdrail],
)    

async def main1():
    try:
        result = await Runner.run(
            agent,
            "Hello, can you help me solve for x: 2x + 3 = 11?",
            run_config=config,
        )
        
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)
        
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
        
async def main2():
    try:
        result = await Runner.run(
            agent,
            "Hello",
            run_config=config,
        )
        
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)
        
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")

async def main3():
    try:
        result = await Runner.run(
            agent,
            "can you solve 2+3 for me",
            run_config=config,
        )
        
        print("Guardrail didn't trip - this is unexpected")
        print(result.final_output)
        
    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")                
                

if __name__ == "__main__":
    print("\nResult 1 :\t")
    asyncio.run(main1())
    
    print("\nResult 2 :\t")
    asyncio.run(main2())
    
    print("\nResult 3 :\t")
    asyncio.run(main3())



