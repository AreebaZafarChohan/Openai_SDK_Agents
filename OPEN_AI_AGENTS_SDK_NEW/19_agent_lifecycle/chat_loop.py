from agents import Agent, Runner, function_tool
from config import config


@function_tool
def get_weather(city: str) -> str:
    """A simple function to get weather for a user"""
    
    return f"The weather of {city.upper()} is sunny."

news_agent: Agent = Agent(
    name="NewsAgent",
    instructions="You are a helpful news assistant.",
)

base_agent: Agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant. If user ask about weather call `get_weather` tool, if user ask about news handoffs to `news_agent` other chat with user and answer user queries. You name is Zehal Khan Afandi and your owner is Miss Areeba Zafar.",
    tools=[get_weather],
    handoffs=[news_agent],
)

user_chat = []

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit", "stop"]:
        break
    
    if user_input.lower() == "view":
        print(f"\nChat History: {user_chat}\n")
        
    user_message = {"role": "user", "content": user_input}    
    user_chat.append(user_message)
    
    res = Runner.run_sync(base_agent, input=user_chat, run_config=config)
    
    assistant_resp = {"role": "assistant", "content": res.final_output}
    user_chat.append(assistant_resp)
    
    print("\nAGENT RESPONSE:", res.final_output)
    
        