import datetime
from agents import Agent, RunContextWrapper, Runner
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
    )
   
    result = Runner.run_sync(
        agent_basic,
        "Hello!",
        run_config=config
    )
    
    print("Basic Dynamic Agent:")
    print(result.final_output)
    
    
    # 🎯 Example 2: Context-Aware Instructions
    print("\n🎭 Example 2: Context-Aware Instructions")
    print("-" * 40)
    
    def context_aware(context: RunContextWrapper, agent: Agent) -> str:
        """Context-aware instructions based on message cound."""
       
        message_count = len(getattr(context, "messages", []))
        
        if message_count == 0:
            return "You are a welcoming assistant. Introduce yourself!"
        
        elif message_count < 3:
            return "You are a helpful assistant. Be encouraging and detailed."
        
        else:
            return "You are an experienced assistant. Be concise but thorough."
     
    agent_context: Agent = Agent(
        name="Context Aware Agent",
        instructions=context_aware,
    )
    
    # Test with multiple messages
    result1 = Runner.run_sync(agent_context, "Hello!", run_config=config)
    print("First message:")
    print(result1.final_output)
    
    result2 = Runner.run_sync(agent_context, "Tell me about python in one line.", run_config=config)
    print("\nSecond message:")
    print(result2.final_output)
    
    
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
    
    
    # 🎯 Example 5: Exploring Context and Agent
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-" * 40)
    
    def explore_context_and_agent(context: RunContextWrapper, agent: Agent) -> str:
        """Explore what's available in context and agent."""
        
        #Access conversation messages
        
        msgs = getattr(context, "messages", [])
        msgs_count = len(msgs)
        
        # Access agent properties
        agent_name = agent.name
        tool_count = len(agent.tools)
        
        return f"""You are {agent_name} with {tool_count} tools. 
        This is message #{msgs_count} in our conversation.
        Be helpful and informative!""" 
    
    agent_explorer: Agent = Agent(
        name="Context Explorer",
        instructions=explore_context_and_agent,
    )
    
    result = Runner.run_sync(
        agent_explorer,
        "What can you tell me about yourself?",
        run_config=config,
    )
    print("Context Explorer Agent:")
    print(result.final_output)    
    
    print("\n🎉 You've learned Dynamic Instructions!")
    print("💡 Try changing the functions and see what happens!")    

if __name__ == "__main__":
    main()    