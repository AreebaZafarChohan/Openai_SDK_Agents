import os
from typing import cast
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, RunContextWrapper, Runner, handoff
from dotenv import load_dotenv
from openai import AsyncOpenAI
import chainlit as cl

# load env file
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY") 


BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

print(f"Loaded API Key: {OPENROUTER_API_KEY is not None}")

# check API KEY is existing or not
if not OPENROUTER_API_KEY:
    raise ValueError("Please ensure that your OPENROUTER_API_KEY is set in .env file.")


gemini_api_key = os.getenv("GEMINI_API_KEY")

print(f"Loaded GEMINI API Key: {gemini_api_key is not None}")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.on_chat_start
async def start():
  #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
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
    
    def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
        agent_name = agent.name
        print("--------------------------------")
        print(f"Handing off to {agent_name}...")
        print("--------------------------------")
        
        # Send a more visible message in the chat
        cl.Message(
            content=f"🔄 **Handing off to {agent_name}...**\n\nI'm transferring your request to our {agent_name.lower()} who will be able to better assist you.",
            author="System"
        ).send() # type: ignore
        
        
    billing_agent = Agent(name="Billing Agent", instructions="You are a billing agent", model=model)
    refund_agent = Agent(name="Refund Agent", instructions="You are a refund agent", model=model)   
    
    
    agent = Agent(
        name="Triage Agent",
        instructions="You are a triage agent",
        model=model,
        handoffs=[
            handoff(billing_agent, on_handoff=lambda ctx: on_handoff(billing_agent, ctx)),
            handoff(refund_agent, on_handoff=lambda ctx: on_handoff(refund_agent, ctx))
        ]
    )
    
    # Set session variables
    
    cl.user_session.set("agent", agent)
    cl.user_session.set("config", config)
    cl.user_session.set("billing_agent", billing_agent)
    cl.user_session.set("refund_agent", refund_agent)
    cl.user_session.set("chat_history", [])
    
    await cl.Message(content="Welcome to the Areeba's AI Assistant! How can I help you today?").send()
    

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    
    # send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()
    
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})

    try:
        result = Runner.run_sync(agent, history, run_config=config)

        response_content = result.final_output

        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # use "developer" instead of "assistant"
        history.append({"role": "developer", "content": response_content})

        # Update session history
        cl.user_session.set("chat_history", history)
        print(f"History: {history}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")
    
    