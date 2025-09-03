import asyncio
from dataclasses import dataclass
from turtle import st
from agents import Agent, Runner, enable_verbose_stdout_logging
from config import config


enable_verbose_stdout_logging()

async def main():
    conversation_history: list = []
    
    agent: Agent = Agent(
        name="Assistant",
        instructions="You are a friendly assistant. Always remember the conversation history.",
    )
    
    print("\nLLM/Agent Context\nAsk anything...")
    
    while True:
        user_input: str = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Ending chat\nGood Bye...\n")
            break
        
        # Convert history into text form
        history_text = "\n".join([f"User: {u}\nAssitant: {a}" for u, a in conversation_history])
        
        # Inject history in LLM Context
        full_prompt = f"{history_text}\nUser: {user_input}\n"
        
        result = await Runner.run(
           agent,
           full_prompt,
           run_config=config, 
        )
        
        llm_reply = result.final_output
        
        print(f"Assitant: {llm_reply}")
        
        # Update history
        conversation_history.append((user_input, llm_reply))
    
if __name__ == "__main__":
    asyncio.run(main())    
    
    
    
    

        