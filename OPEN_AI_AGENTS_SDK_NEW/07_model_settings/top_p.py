from agents import Agent, ModelSettings, Runner, enable_verbose_stdout_logging
from config import config

# enable_verbose_stdout_logging()

# ====== 1. TOP-P EXPERIMENT ======
top_p_high_agent = Agent(
    name="Top-p High",
    instructions="Be creative and diverse.",
    model_settings=ModelSettings(max_tokens=100, top_p=0.95, temperature=0.8)
)

top_p_medium_agent = Agent(
    name="Top-p Medium",
    instructions="Balanced diversity.",
    model_settings=ModelSettings(max_tokens=100, top_p=0.7, temperature=0.8)
)

top_p_low_agent = Agent(
    name="Top-p Low",
    instructions="Be focused and predictable.",
    model_settings=ModelSettings(max_tokens=100, top_p=0.3, temperature=0.8)
)

# ====== 2. PENALTIES EXPERIMENT ======
freq_penalty_agent = Agent(
    name="Frequency Penalty Only",
    instructions="Avoid repeating words.",
    model_settings=ModelSettings(
        max_tokens=100,
        # frequency_penalty=0.5,
        temperature=0.8
    )
)

presence_penalty_agent = Agent(
    name="Presence Penalty Only",
    instructions="Encourage new topics in writing.",
    model_settings=ModelSettings(
        max_tokens=100,
        presence_penalty=0.3,
        temperature=0.8
    )
)

both_penalties_agent = Agent(
    name="Both Penalties",
    instructions="Avoid repetition and explore new topics.",
    model_settings=ModelSettings(
        max_tokens=100,
        # frequency_penalty=0.5,  # Avoid repeating words
        presence_penalty=0.3,     # Encourage new topics
        temperature=0.8
    )
)


prompt = "Write a paragraph about Pakistan's culture and history."

# ====== RUN FUNCTION ======
def run_and_print(agent_list, title):
    print("\n" + "="*30 + f" {title} " + "="*30 + "\n")
    for agent in agent_list:
        print(f"--- {agent.name} ---")
        result = Runner.run_sync(agent, prompt, run_config=config)
        print(result.final_output, "\n")
        if hasattr(result, "usage"):
            print(f"Tokens Used: {getattr(result.usage, 'total_tokens', 'N/A')}") # type: ignore
        print("\n" + "-"*60 + "\n")

# Run experiments
run_and_print([top_p_high_agent, top_p_medium_agent, top_p_low_agent], "TOP-P COMPARISON")
run_and_print([freq_penalty_agent, presence_penalty_agent, both_penalties_agent], "PENALTIES COMPARISON")