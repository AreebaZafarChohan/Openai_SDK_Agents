import asyncio
from agents import SQLiteSession


async def memory_operations_demo():
    session = SQLiteSession("memory_ops", "test.db")
    
    conversation_items = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I assist you today?"},
        {"role": "user", "content": "What's the weather like?"},
        {"role": "assistant", "content": "I don't have access to weather data."},
    ]
    
    await session.add_items(conversation_items) # type: ignore
    print("\nAdded items to session.")
    
    items = await session.get_items()
    
    print("\nMemory Cpntains {len(items)} itesms:")
    for item in items:
        print(f"- {item['role']}: {item['content']}") # type: ignore
        
    last_item = await session.pop_item()
    print(f"\nRemoved last item: {last_item}")   
    
    items = await session.get_items()
    
    print("\nMemory now Cpntains {len(items)} itesms:")
    for item in items:
        print(f"- {item['role']}: {item['content']}") # type: ignore 
    
    await session.clear_session()
    
    print("\nCleared session.")
    
    items = await session.get_items()
    print(f"\nMemory now contains {len(items)} items.")
    
asyncio.run(memory_operations_demo())    