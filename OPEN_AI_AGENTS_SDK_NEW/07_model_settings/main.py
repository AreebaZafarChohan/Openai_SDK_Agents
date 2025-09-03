from agents import Agent, Runner, function_tool, ModelSettings, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

@function_tool
def calculate_area(length: float, width: float) -> str:
    """Calculate the area of a rectangle"""
    area = length * width
    return f"Area = {length} * {width} = {area} square units."

@function_tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return its result"""
    return a * b


math_agent = Agent(
        name="Math Agent",
        instructions="""
            You are a mathematics specialist.
            If the user asks for calculations, use `calculate_area` or `multiply`.
            After using tools, also provide detailed explanations for *all* questions asked.
        """,
        tools=[calculate_area, multiply],
        model_settings=ModelSettings(
            temperature=0.7,
            top_p=0.9,
            max_tokens=1000,
            presence_penalty=0.3,
    ),
)
    
urdu_agent = Agent(
        name="Urdu Agent",
        instructions="You are a urdu specialist.",
        tools=[calculate_area, multiply],
        model_settings=ModelSettings(
            temperature=1.9,
            top_p=0.9,
            max_tokens=1000,
            tool_choice="none",
            presence_penalty=1.9
    ),
)

def main():
    """Learn Model Settings with simple examples."""
    
    print("\n❄️  🔥 Model Settings ")
    print("-" * 30)
    
    question1 = """
                1. What is a + b square formula, why we use it.
                2. Calculate the area of rectangle 35cm width and 84cm length.
                3. What is 95 * 48?"""
    question2 = """Write an emotional drama in roman urdu."""
    
    print("Math Agent:  temperature=0.1, top_p=0.5, max_tokens=1000, presence_penalty=-1.5 ")
    result_math = Runner.run_sync(math_agent, question1, run_config=config)
    print(result_math.final_output)
    
    print("\nUrdu Agent: Temperature = 1.9, top_p=0.9, max_tokens=1000, tool_choice='none', presence_penalty=-1.9 ")
    result_urdu = Runner.run_sync(urdu_agent, question2, run_config=config)
    print(result_urdu.final_output)
    
    print("📝 Note: Gemini temperature range extends to 2.0")
    
if __name__ == "__main__":
    main()    