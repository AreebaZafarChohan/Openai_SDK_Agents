import os
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import cast
from agents.run import RunConfig
import chainlit as cl

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# https://generativelanguage.googleapis.com/v1beta/openai/

@cl.on_chat_start
async def start():
    
    external_client = AsyncOpenAI(
        api_key = GEMINI_API_KEY,
        base_url= "https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client,
    )
    
    config = RunConfig(
        model = model,
        model_provider = external_client, # type: ignore
        tracing_disabled = True
    )
    
    # Initialize chat history
    
    cl.user_session.set("chat_history", [])
    
    cl.user_session.set("config", config)
    
    agent: Agent = Agent(name="Areeba's Assistant", instructions="You are a helping asssitant. Your name is Arhaam Khanzada. Your owner is Areeba Zafar.", model=model)
    
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Assalam o alaikum. I'm Arhaam Khanzada! How may I help you today?").send()
    
@cl.on_message
async def main(message: cl.Message):
    
    # Getting chat history from user session
    history = cl.user_session.get("chat_history") or []
    
    # append the user's message in the history
    history.append({"role": "user", "content": message.content})
    
    
    # create a new message object for streaming
    msg = cl.Message(content="")
    await msg.send()
    
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    
    try:
        print(f"\nCalling_AGENT_WITH_CONTEXT_AND_STREAMING\n {history} \n")
        
         # Run the agent with streaming enabled
        result = Runner.run_streamed(agent, history, run_config=config)

        # Stream the response token by token
        
        async for event in result.stream_events():
            if event.type == "raw_response_event" and hasattr(event.data, "delta"):
                token = event.data.delta # type: ignore
                await msg.stream_token(token) # type: ignore
                
        history.append({"role": "assistant", "content": msg.content})
        
        cl.user_session.set("chat_history", history)
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {msg.content}")
        
    except Exception as e:
        await msg.update(content=f"Error: {str(e)}") # type: ignore
        print(f"Error: {str(e)}")  
    
    