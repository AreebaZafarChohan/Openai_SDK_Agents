from typing import Any, List
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
# INPUT GUARDRAILS
# -----------------

@input_guardrail
async def profanity_filter(ctx: RunContextWrapper, agent: Agent, input: str | List[TResponseInputItem]) -> GuardrailFunctionOutput:
    if any(bad in str(input).lower() for bad in ["badword1", "badword2"]):
        return GuardrailFunctionOutput(output_info="Profanity detected", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Clean input", tripwire_triggered=False)


@input_guardrail
async def topic_validator(ctx: RunContextWrapper, agent: Agent, input: str | List[TResponseInputItem])  -> GuardrailFunctionOutput:
    if "agents sdk" not in str(input).lower():
        return GuardrailFunctionOutput(output_info="Off-topic", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="On-topic", tripwire_triggered=False)


@input_guardrail
async def rate_limiter(ctx: RunContextWrapper, agent: Agent, input: str | List[TResponseInputItem])  -> GuardrailFunctionOutput:
    user_id = getattr(ctx.context, "user_id", "guest")

    recent_requests = getattr(ctx.context, "recent_requests", {})

    count = recent_requests.get(user_id, 0)

    if count > 5:
        return GuardrailFunctionOutput(
            output_info=f"Too many requests by {user_id}",
            tripwire_triggered=True
        )
    return GuardrailFunctionOutput(output_info="Rate OK", tripwire_triggered=False)


# -----------------
# OUTPUT GUARDRAILS
# -----------------

@output_guardrail
async def privacy_checker(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    if "ssn" in str(output).lower():
        return GuardrailFunctionOutput(output_info="Sensitive info detected", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Safe output", tripwire_triggered=False)


@output_guardrail
async def quality_validator(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    if len(str(output)) < 10:  # too short
        return GuardrailFunctionOutput(output_info="Low quality", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Good quality", tripwire_triggered=False)


@output_guardrail
async def brand_compliance(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    if "competitor" in str(output).lower():
        return GuardrailFunctionOutput(output_info="Brand violation", tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info="Brand OK", tripwire_triggered=False)


# -----------------
# MAIN AGENT
# -----------------

agent = Agent(
    name="Multi-Protected Agent",
    instructions="Answer questions about OpenAI Agents SDK.",
    input_guardrails=[profanity_filter, topic_validator, rate_limiter],
    output_guardrails=[privacy_checker, quality_validator, brand_compliance],
)

def main():
    test_cases = [
        ("Normal valid input", "Tell me about the Agent Loop in Agents SDK."),
        ("Profanity input", "This is badword1 in Agents SDK."),
        ("Off-topic input", "What is the capital of France?"),
        ("Rate limit exceeded", "Agents SDK explanation please."),
    ]

    outputs_to_test = [
        ("Safe output", "The Agent Loop is the cycle where the agent observes → decides → acts."),
        ("Too short output", "Okay."),
        ("Sensitive output", "The user SSN is 123-45-6789."),
        ("Brand violation", "Our competitor is better than us."),
    ]

    print("\n--- INPUT GUARDRAIL TESTS ---")
    for label, inp in test_cases:
        try:
            result = Runner.run_sync(agent, inp, run_config=config)
            print(f"[{label}] ✅ Passed → {result.final_output}")
        except InputGuardrailTripwireTriggered as e:
            print(f"[{label}] 🚨 Input blocked → {e}")
        except OutputGuardrailTripwireTriggered as e:
            print(f"[{label}] 🚨 Output blocked → {e}")

    print("\n--- OUTPUT GUARDRAIL TESTS ---")
    for label, out in outputs_to_test:
        try:
            # Directly run output guardrail simulation
            result = Runner.run_sync(agent, "Agents SDK explanation", run_config=config)
            # Inject fake output
            fake = Runner.run_sync(agent, out, run_config=config)
            print(f"[{label}] ✅ Output allowed → {fake.final_output}")
        except OutputGuardrailTripwireTriggered as e:
            print(f"[{label}] 🚨 Output blocked → {e}")
        except InputGuardrailTripwireTriggered as e:
            print(f"[{label}] 🚨 Input blocked → {e}")    


if __name__ == "__main__":
    main()