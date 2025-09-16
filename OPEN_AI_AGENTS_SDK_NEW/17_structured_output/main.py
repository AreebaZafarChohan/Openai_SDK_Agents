from pydantic import BaseModel
from agents import Agent, Runner
from config import config

class WeatherAnswer(BaseModel):
    location: str
    temperature_c: float
    summary: str 

agent = Agent(
    name="WeatherInfoExtractor",
    instructions="Extract weather information from the user's message.",
    output_type=WeatherAnswer  # This is the magic!
)

# Test it
result = Runner.run_sync(
    agent, 
    "What's the weather like in Karachi City today?",
    run_config=config
)

print(result.final_output.location)      
print(result.final_output.temperature_c) 
print(result.final_output.summary)