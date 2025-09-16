from pdb import run
from typing import List
from config import config
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail,
)

# -----------------
# INPUT GUARDRAIL
# -----------------
@input_guardrail
async def context_aware_guardrail(ctx: RunContextWrapper, agent: Agent, input: str | List[TResponseInputItem]) -> GuardrailFunctionOutput:
    user_context = ctx.context.get("user_history", {})
    suspicious = user_context.get("suspicious_activity", False)

    if suspicious:
        if "quiz" in str(input).lower():
            return GuardrailFunctionOutput(
                output_info="Suspicious user trying quiz solving",
                tripwire_triggered=True
            )
    return GuardrailFunctionOutput(
        output_info="Safe input",
        tripwire_triggered=False
    )


# -----------------
# OUTPUT GUARDRAIL
# -----------------
@output_guardrail
async def context_aware_output_guardrail(ctx: RunContextWrapper, agent: Agent, output: str) -> GuardrailFunctionOutput:
    session_flags = ctx.context.get("flags", {})
    strict_mode = session_flags.get("strict_mode", False)

    if strict_mode and "answer" in str(output).lower():
        return GuardrailFunctionOutput(
            output_info="Blocked due to strict mode",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info="Output allowed", tripwire_triggered=False)


# -----------------
# MAIN AGENT
# -----------------
agent = Agent(
    name="ContextAwareAgent",
    instructions="You are a teaching agent for the OpenAI Agents SDK.",
    input_guardrails=[context_aware_guardrail],
    output_guardrails=[context_aware_output_guardrail],
)


# -----------------
# TEST SCENARIOS
# -----------------
def main():
    # 1. Normal user, safe query
    try:
        result = Runner.run_sync(
            agent,
            "Explain the Agent Loop in Agents SDK",
            context={"context": {"user_history": {"suspicious_activity": False}, "flags": {"strict_mode": False}}},
            run_config=config,
        )
        print("Case 1 ✅:", result.final_output)
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print("Case 1 🚨 Blocked:", e)

    # 2. Suspicious user trying quiz
    try:
        result = Runner.run_sync(
            agent,
            "Solve this quiz about Agents SDK",
            context={"context": {"user_history": {"suspicious_activity": True}, "flags": {"strict_mode": False}}},
            run_config=config,
        )
        print("Case 2 ✅:", result.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Case 2 🚨 Input Blocked:", e)

    # 3. Strict mode ON and output contains 'answer'
    try:
        result = Runner.run_sync(
            agent,
            "Give me the answer about Agents SDK",
            run_config=config,
            context={"context": {"user_history": {"suspicious_activity": False}, "flags": {"strict_mode": True}}}
        )
        print("Case 3 ✅:", result.final_output)
    except OutputGuardrailTripwireTriggered as e:
        print("Case 3 🚨 Output Blocked:", e)

    # 4. Strict mode OFF, same query allowed
    try:
        result = Runner.run_sync(
            agent,
            "Give me the answer about Agents SDK",
            context={"context": {"user_history": {"suspicious_activity": False}, "flags": {"strict_mode": False}}},
            run_config=config,
        )
        print("Case 4 ✅:", result.final_output)
    except (InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered) as e:
        print("Case 4 🚨 Blocked:", e)


if __name__ == "__main__":
    main()
