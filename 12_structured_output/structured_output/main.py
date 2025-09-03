import asyncio
from config import config
from agents import Agent, Runner
from pydantic import BaseModel

class WeatherAnswer(BaseModel):
    location: str
    temperature_c: float
    summary: str

agent : Agent = Agent(
    name="StructuredWeatherAgent",
    instructions="Use the final_output tool with WeatherAnswer schema.",
    output_type=WeatherAnswer
)

async def main():
    result = await Runner.run(agent, "Tell me karachi's temperature?.", run_config=config)
    
    print(result.final_output)
    print(result.final_output.temperature_c)
    print(type(result.final_output))

asyncio.run(main())    