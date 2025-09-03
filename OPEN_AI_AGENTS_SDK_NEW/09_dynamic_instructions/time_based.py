import datetime
from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 3: Time-Based Instructions
    print("\n🎭 Example 3: Time-Based Instructions")
    print("-" * 40)
    
    def time_based(context: RunContextWrapper, agent: Agent) -> str:
        """Time-based  instructions based on current hour."""
        current_hour = datetime.datetime.now().hour
       
        if 6 <= current_hour < 12:
            return f"You are {agent.name}. Good morning! Be energetic and positive."
        elif 12 <= current_hour < 17:
            return f"You are {agent.name}. Good afternoon! Be focused and productive."
        else:
            return f"You are {agent.name}. Good evening! Be calm and helpful."

    agent_time: Agent = Agent(
        name="Time Aware Agent",
        instructions=time_based,
    )
   
    result = Runner.run_sync(
        agent_time,
        "How are you today?",
        run_config=config
    )
    
    print("Time-Based Agent:")
    print(result.final_output)
    

if __name__ == "__main__":
    main()    