
from agents import Agent, function_tool

@function_tool
def calculate_area(length: float, width: float) -> str:
    return f"Area = {length * width} square units"

# Demonstrate shared references
original_agent = Agent(
    name="Original",
    tools=[calculate_area],
    instructions="You are helpful."
)

# Clone without new tools list
shared_clone = original_agent.clone(
    name="SharedClone",
    instructions="You are creative."
)

# Add tool to original
@function_tool
def new_tool() -> str:
    return "I'm a new tool!"

original_agent.tools.append(new_tool)

# Add another tool
@function_tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny, 72°F"

original_agent.tools.append(get_weather)

# Check if clone also has the new tool
print("Original tools:", len(original_agent.tools))  # 3
print("Clone tools:", len(shared_clone.tools))      # 3 (shared!)

# Create independent clone
independent_clone = original_agent.clone(
    name="IndependentClone",
    tools=[calculate_area],  # New list
    instructions="You are independent."
)

original_agent.tools.append(new_tool)
print("Independent clone tools:", len(independent_clone.tools))  # 1 (independent!)