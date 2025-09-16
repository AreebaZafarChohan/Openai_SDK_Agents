from typing import Any, Optional
from config import config
from agents import Agent, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered, RunContextWrapper, Runner, input_guardrail, output_guardrail
from pydantic import BaseModel, Field


# class WeatherSanitizer(BaseModel):
#     weather_related: bool
#     reason: str | None = None

# class WeatherSanitizer(BaseModel):
#     weather_related: bool = Field(..., description="True if query is about weather, else False")
#     reason: Optional[str] = Field(None, description="Why the query is or is not weather related")

class WeatherSanitizer(BaseModel):
    weather_related: bool
    reason: str
    
weather_sanitizer = Agent(
    name="WeatherSanitizer",
    instructions="Check if this is a weather related query",
    output_type=WeatherSanitizer
)    

@input_guardrail
async def weather_input_checker(ctx: RunContextWrapper, agent: Agent, input) -> GuardrailFunctionOutput:
    res = await Runner.run(weather_sanitizer, input, run_config=config)
    print("\n[WEATHER SANITIZER RESPONSE]", res.final_output)
    return GuardrailFunctionOutput(
        output_info="passed",
        tripwire_triggered=res.final_output.weather_related is False
    )
    
@output_guardrail
def weather_response_checker(ctx: RunContextWrapper, agent: Agent, output: Any) -> GuardrailFunctionOutput:
    return GuardrailFunctionOutput(
        output_info="passed",
        tripwire_triggered=False
    )

agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant.",
    input_guardrails=[weather_input_checker],
    output_guardrails=[weather_response_checker],
)    

try:
    res = Runner.run_sync(
        # agent, [{"role": "user", "content": "What's the weather like in SF?"}], run_config=config
        agent, "What's the weather like in SF?", run_config=config

    )
    print("[OUTPUT]", res.to_input_list)
    print("[FINAL OUTPUT]", res.final_output)
except InputGuardrailTripwireTriggered as e:
    print(f"Alert: Guardrail input tripwire was triggered!\nError: {e}")
except OutputGuardrailTripwireTriggered as e:
    print(f"Alert: Guardrail output tripwire was triggered!\nError: {e}")    
            
print(f"\n\n{"*"*50}\n\n")
            
try:
    res = Runner.run_sync(
        # agent, [{"role": "user", "content": "What's the weather like in SF?"}], run_config=config
        agent, "What is pydantic in programming?", run_config=config

    )
    print("[OUTPUT]", res.to_input_list)
    print("[FINAL OUTPUT]", res.final_output)
except InputGuardrailTripwireTriggered as e:
    print(f"Alert: Guardrail input tripwire was triggered!\nError: {e}")
except OutputGuardrailTripwireTriggered as e:
    print(f"Alert: Guardrail output tripwire was triggered!\nError: {e}")             
