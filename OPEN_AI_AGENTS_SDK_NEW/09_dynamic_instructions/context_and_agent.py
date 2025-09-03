from agents import Agent, RunContextWrapper, Runner, enable_verbose_stdout_logging
from config import config

enable_verbose_stdout_logging()

# Store full conversation history
conversation_history = []

def main():
    """Learn Dynamic Instructions with simple examples."""
    print("🎭 Dynamic Instructions: Make Your Agent Adapt")
    print("=" * 50)
    
    # 🎯 Example 5: Exploring Context and Agent
    print("\n🎭 Example 5: Exploring Context and Agent")
    print("-" * 40)
    
    def explore_context_and_agent(context: RunContextWrapper, agent: Agent) -> str:
        """Explore what's available in context and agent."""
        
        # # Access conversation messages from context
        # msgs = getattr(context, "messages", [])
        # msgs_count = len(msgs)
        
        msgs_count = len(conversation_history) // 2  # manual history count
        
        # Access agent properties
        agent_name = agent.name
        tool_count = len(agent.tools)
        
        return f"""You are {agent_name} with {tool_count} tools. 
                   This is message #{msgs_count} in our conversation.
                   Be helpful and informative!
                """
    
    agent_explorer: Agent = Agent(
        name="Context Explorer",
        instructions=explore_context_and_agent,
    )

    # Helper function to send message with history
    def send_message(user_message: str):
        conversation_history.append({"role": "user", "content": user_message})
        result = Runner.run_sync(agent_explorer, conversation_history, run_config=config)
        conversation_history.append({"role": "assistant", "content": result.final_output})
        return result.final_output

    # First message
    print("Context Explorer Agent:")
    print(send_message("What can you tell me about yourself in one line?"))
    
    print("="*70)
    
    # Multiple interactions
    for i in range(4):
        print(f"Interaction {i+1}:")
        output = send_message(f"Question {i+1}: Tell me about AI in 2 lines.")
        print(output[:100] + "...")
        print()
    
    # Show final conversation history
    print("📝 Final Conversation History:")
    for msg in conversation_history:
        print(f"{msg['role'].capitalize()}: {msg['content']}")

if __name__ == "__main__":
    main()
