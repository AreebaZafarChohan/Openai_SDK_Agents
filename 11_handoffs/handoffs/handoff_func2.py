import asyncio
from agents import Agent, RunContextWrapper, Runner, handoff
from config import config

urdu_agent = Agent(
    name="Urdu Agent",
    instructions="You are an Urdu language expert. Respond only in fluent Urdu. Translate any input into Urdu."
)

english_agent = Agent(
    name="English Agent",
    instructions="You are an English language expert. Respond only in fluent English. Translate any input into English."
)

punjabi_agent = Agent(
    name="Punjabi Agent",
    instructions="You are an Punjabi language expert. Respond only in fluent Punjabi. Translate any input into Punjabi."
)

pashto_agent = Agent(
    name="Pashto Agent",
    instructions="You are an Pashto language expert. Respond only in fluent Pashto. Translate any input into Pashto."
)

korean_agent = Agent(
    name="Korean Agent",
    instructions="You are an Korean language expert. Respond only in fluent Korean. Translate any input into Korean."
)

def on_handoff(agent: Agent, ctx: RunContextWrapper[None]):
    agent_name = agent.name
    print("--------------------------------")
    print(f"Handing off to {agent_name}...")
    print("--------------------------------")
    
triage_agent = Agent(
    name="Triage agent",
    instructions=(
        "Detect the language of the input and handoff to the corresponding language agent. "
        "If the message is in Urdu, handoff to Urdu Agent. "
        "If in English, handoff to English Agent. "
        "If in Punjabi, handoff to Punjabi Agent. "
        "If in Pashto, handoff to Pashto Agent. "
        "If in Korean, handoff to Korean Agent."
        ),
    handoffs=[
        handoff(urdu_agent, on_handoff=lambda ctx: on_handoff(urdu_agent, ctx)),
        handoff(english_agent, on_handoff=lambda ctx: on_handoff(english_agent, ctx)),
        handoff(punjabi_agent, on_handoff=lambda ctx: on_handoff(punjabi_agent, ctx)),
        handoff(pashto_agent, on_handoff=lambda ctx: on_handoff(pashto_agent, ctx)),
        handoff(korean_agent, on_handoff=lambda ctx: on_handoff(korean_agent, ctx)),
    ]
)     
    
async def main(input: str):
    result = await Runner.run(triage_agent, input=input, run_config=config)
    print(result.final_output)    

asyncio.run(main("Hello my friend, how are you?"))

# 1. English:
# Peace be upon you, how are you my friend?

# 2. Urdu:
# السلام علیکم، آپ کیسے ہیں دوست؟

# 3. Pashto (پښتو):
# السلام علیکم، ته څنګه یې زما ملګری؟
# (Assalam o Alaikum, ta tsenga ye zama malgari?)

# 4. Punjabi (Shahmukhi / Urdu script):
# السلام علیکم، تُسیں کیویں ہو دوست؟
# (Assalam o Alaikum, tusi kiven ho dost?)

# 5. Korean (Romanized + Hangul):
# 안녕하세요, 친구야 잘 지냈어?
# (Annyeonghaseyo, chinguya jal jinaesseo?)
# Meaning: "Hello, my friend. How have you been?"

# 6. Arabic:
# السلام عليكم، كیف حالك یا صدیقي؟    