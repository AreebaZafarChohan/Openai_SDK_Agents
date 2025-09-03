from agents import Agent, ModelSettings, Runner
from config import config

focused_agent: Agent = Agent(
    name="Fact_Agent",
    instructions="You work is to tell facts.",
    model_settings=ModelSettings(temperature=0.2),
)

topics_explainer: Agent = Agent(
    name="Tpoics_Explainer",
    instructions="""You are a precise topics explainer.""",
    model_settings=ModelSettings(temperature=0.5),
)

creative_agent: Agent = Agent(
    name="Short_Novels_Writer",
    instructions="""You work is to create short novels in roman urdu.""",
    model_settings=ModelSettings(temperature=1.9)
)
    
print("Focused Agent (Temperature = 0.2):")
result_focused = Runner.run_sync(focused_agent,"Tell me about some facts of world.", run_config=config)
print(result_focused.final_output)
print("\n","="*70, "\n")

print("\n Topics Explainer Agent (Temperature = 0.5):")
result_topics = Runner.run_sync(topics_explainer,"Tell me about in short what is web development.", run_config=config)
print(result_topics.final_output)

print("\n","="*70, "\n")


print("\n Creative Agent (Temperature = 1.9):")
result_creative = Runner.run_sync(creative_agent,"Create a funny and friendship based novel with success moral.", run_config=config)
print(result_creative.final_output)

print("\n","="*70, "\n")

print("\n💡 Notice: Focused = Math, facts, precise instructions (LOW 0.1 - 0.3), Topics Explainer = General conversation, explanations (MEDIUM 0.4 - 0.6) , Creative = Creative writing, brainstorming (HIGH 0.7 - 0.9)")
print("📝 Note: Gemini temperature rangeextends to 2.0")