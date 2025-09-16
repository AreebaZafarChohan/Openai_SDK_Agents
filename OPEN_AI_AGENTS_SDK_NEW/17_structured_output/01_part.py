from pydantic import BaseModel
from agents import Agent, Runner
from config import config

# Define your data structure
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

# Create agent with structured output
agent = Agent(
    name="InfoCollector",
    instructions="Extract person information from the user's message.",
    output_type=PersonInfo  # This is the magic!
)

# Test it
result = Runner.run_sync(
    agent, 
    "Hi, I'm Alice, I'm 25 years old and I work as a teacher.",
    run_config=config
)

# Now you get perfect structured data!
print("Type:", type(result.final_output))        # <class 'PersonInfo'>
print("Name:", result.final_output.name)         # "Alice"
print("Age:", result.final_output.age)           # 25
print("Job:", result.final_output.occupation)    # "teacher"