import asyncio
from typing import Any
from agents import Agent, ModelSettings, RunContextWrapper, function_tool, Runner
from config import config

# @function_tool
# def get_weather_alternative(city: str) -> str:
#     """Fallback weather service (used if primary service fails)"""
#     return f"[Alternative Service] The weather information for {city} is not available at the moment."

def weather_failure_handler(exception: Exception, ctx: RunContextWrapper[Any], args=None):
    """Custom error handler to fallback to alternative service."""

    city = "Unknown"
    if args and "city" in args:
        city = args["city"]
        
    print(f"[Error Handler] Primary weather service failed: {exception}") 
    
@function_tool(description_override="", failure_error_function=weather_failure_handler) # type: ignore
def get_weather(city: str) -> str:
    try:
       raise TimeoutError("Primary weather service did not respond in time.")
    except ValueError:
        raise ValueError("Weather service is currently unavailable.")
    except TimeoutError:
        raise TimeoutError("Weather service request timed out.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

base_agent: Agent = Agent(
    name="Base Agent",
    instructions="You are a helpfull agent.",
    tools=[get_weather],
    # model_settings=ModelSettings(tool_choice="required"),
    tool_use_behavior="stop_on_first_tool"
)
    
async def main():
    print("--- First Run ---")
    res = await Runner.run(base_agent, "What is weather in Lahore?", run_config=config)
    print(f"Final Output: {res.final_output}")

    print("\n--- Second Run ---")
    res2 = await Runner.run(base_agent, "What is the full form of AI?", run_config=config)
    print(f"Final Output: {res2.final_output}")
    
if __name__ == "__main__":
    asyncio.run(main())
    