from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 4: Stateful Instructions (Remembers)
    print("\n🎭 Example 4: Stateful Instructions")
    print("-" * 40)
    
    class StatefulInstructions:
        """Statefu instructions that remember interaction count"""
        
        def __init__(self) -> None:
            self.interaction_count = 0
        
        def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
            self.interaction_count += 1
            
            if self.interaction_count == 1:
                return "You are a learning assistant. This is our first interaction - be welcoming!"
            elif self.interaction_count <= 3:
                return f"You are a learning assistant. This is interaction #{self.interaction_count} - build on our conversation."
            else:
                return f"You are an experienced assistant. We've had {self.interaction_count} interactions - be efficient."
            
    instruction_gen = StatefulInstructions()    
    
    agent_stateful: Agent = Agent(
        name="Stateful Agent",
        instructions=instruction_gen,
    )
    
    # Test multiple interactions
    
    for i in range(4):
        result = Runner.run_sync(agent_stateful, f"Question {i+1}: Tell me about AI", run_config=config)
        print(f"Interaction {i+1}:")
        print(result.final_output[:100] + "...")
        print()

if __name__ == "__main__":
    main()    