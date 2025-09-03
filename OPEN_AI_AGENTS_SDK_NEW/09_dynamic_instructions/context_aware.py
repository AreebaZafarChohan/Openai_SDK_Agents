from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging
from config import config

enable_verbose_stdout_logging()

# Global shared context list
conversation_history = []


def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 2: Context-Aware Instructions
    print("\n🎭 Example 2: Context-Aware Instructions")
    print("-" * 40)
    
    def context_aware(context: RunContextWrapper, agent: Agent) -> str:
        """Context-aware instructions based on message cound."""
       
        message_count = len(conversation_history) // 2
        
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
    
    # Function to send message and update history
    def send_message(user_message: str):
        conversation_history.append({"role": "user", "content": user_message})
        result = Runner.run_sync(agent_context, user_message, run_config=config)
        conversation_history.append({"role": "assistant", "content": result.final_output})
        return result.final_output

    # Test sequence
    print("First message:", send_message("Hello!"))
    print("\nSecond message:", send_message("Tell me about Python in one line."))
    print("\nThird message:", send_message("How are you?"))
    print("\nFourth message:", send_message("Tell me about Karachi in one line."))
    print("\nFifth message:", send_message("Tell me about Quaid-e-Azam in one line."))
    

if __name__ == "__main__":
    main()    