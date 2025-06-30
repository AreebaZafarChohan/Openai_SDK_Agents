import os
from dotenv import load_dotenv
from typing import cast
import chainlit as cl
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from agents.run import RunConfig

# load the enivronment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the api key is present or not
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    
    external_client = AsyncOpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    
    config = RunConfig(
        model=model,
        model_provider=external_client, # type: ignore
        tracing_disabled=True
    )
    
    #Initialize an empty chat history in session
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    
    agent: Agent = Agent(name="Areeba's Assitant", instructions="You are a helping assistant. Your name is Zehal Khan Afandi and your owner is Areeba Zafar and your gender is male. You will response like a professional or good friend in english and also in roman urdu along with emojis.", model=model)
    
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Hello My name is Zehal Khan Afandi ❤ How can I help you today?").send()
    
@cl.on_message
async def main(message: cl.Message):
    # send thinking message
    msg = cl.Message(content="Thinking")
    await msg.send()
    
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config")) 
    
    #Retrieve the chat history from session
    history = cl.user_session.get("chat_history") or []
    
    history.append({"role": "user", "content": message.content})  
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(starting_agent = agent,
                    input=history,
                    run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", result.to_input_list())
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")