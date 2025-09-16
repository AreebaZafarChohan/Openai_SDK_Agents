from typing import Any, List
from openai import BaseModel
from pydantic import ConfigDict
from config import config
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, RunContextWrapper, Runner, TResponseInputItem, input_guardrail, output_guardrail


class AgentsSDKQuiz(BaseModel):
    is_agents_sdk_quiz : bool
    reason: str
    
    model_config = ConfigDict(extra="forbid")

input_guardrail_agent = Agent(
    name="Agents SDK Quiz Checker",
    instructions=(
        "Classify the input:\n"
        "- If the user is giving a multiple-choice question (MCQ), quiz, or asking to SOLVE/ANSWER a quiz about Agents SDK → set is_agents_sdk_quiz=True.\n"
        "- If the user is asking for explanation, teaching, or concepts about Agents SDK → set is_agents_sdk_quiz=False.\n"
        "- If the input is unrelated (like general knowledge) → set is_agents_sdk_quiz=False."
    ),
    output_type=AgentsSDKQuiz
)

@input_guardrail
async def input_checker(ctx: RunContextWrapper, agent: Agent, input: str | List[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    result = await Runner.run(input_guardrail_agent, input, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_agents_sdk_quiz
    )

output_guardrail_agent = Agent(
    name="Output Checker",
    instructions=(
        "Classify the output:\n"
        "- If the output contains solving or answering a quiz about Agents SDK (like choosing A/B/C/D) → set is_agents_sdk_quiz=True.\n"
        "- If the output is just explanation, teaching, or unrelated → set is_agents_sdk_quiz=False."
    ),
    output_type=AgentsSDKQuiz
)


@output_guardrail
async def output_checker(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    result = await Runner.run(output_guardrail_agent, output, run_config=config)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_agents_sdk_quiz
    )

teacher_agent = Agent(
    name="Teacher Agent",
    instructions="You are a teacher agent helping students with their queries.",
    input_guardrails=[input_checker],
    output_guardrails=[output_checker]
)

    
try:
    # Allowed (explanation)
    result1 = Runner.run_sync(teacher_agent, "What is the Agent Loop in Agents SDK? Describe me in short.", run_config=config)
    print("Result 1:", result1.final_output)

    # Allowed (general knowledge)
    result2 = Runner.run_sync(teacher_agent, "What is the capital of France?", run_config=config)
    print("Result 2:", result2.final_output)

    # Blocked (quiz solving request)
    result3 = Runner.run_sync(teacher_agent, """
        Solve this quiz:
        Q. What is the main purpose of the OpenAI Agents SDK?
        A) Only to run models
        B) To build agents with tools, memory, and policies
        C) To label datasets
        D) Only to generate API keys
    """, run_config=config)
    print("Result 3:", result3.final_output)

except InputGuardrailTripwireTriggered as e:
    print("⚠️ Input Guardrail Triggered:", e)

except OutputGuardrailTripwireTriggered as e:
    print("⚠️ Output Guardrail Triggered:", e)
      
    