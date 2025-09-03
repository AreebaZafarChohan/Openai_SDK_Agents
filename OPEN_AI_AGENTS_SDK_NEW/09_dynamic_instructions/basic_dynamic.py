from agents import Agent, ModelSettings, RunContextWrapper, Runner
from config import config


def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 1: Basic Dynamic Instructions
    print("\n🎭 Example 1: Basic Dynamic Instructions")
    print("-" * 40)
    
    def basic_dynamic(context: RunContextWrapper, agent: Agent) -> str:
       """Basic dynamic instructions function."""
       return f"You are {agent.name}. Be helpful and friendly."
   
    agent_basic: Agent = Agent(
        name="Dynamic Agent",
        instructions=basic_dynamic,
        model_settings=ModelSettings()
    )
   
    result = Runner.run_sync(
        agent_basic,
        "Hello!",
        run_config=config
    )
    
    print("Basic Dynamic Agent:")
    print(result.final_output)
    

if __name__ == "__main__":
    main()    