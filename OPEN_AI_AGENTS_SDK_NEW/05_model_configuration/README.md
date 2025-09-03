# Configuring LLM Providers at Different Levels (Global, Run, and Agent)

The **Agents SDK** is setup to use **OpenAI** as the default provider.  
When using other providers (like **Gemini**), you can configure them at **different levels**:

- **Agent Level**
- **Run Level**
- **Global Level**

We will always prioritize your **Agent Level Configuration**, so each agent can use the LLM best suited for it.

---

## 1. Agent Level

```python
import asyncio
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled

gemini_api_key = ""

# Reference: https://ai.google.dev/gemini-api/docs/openai
client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

set_tracing_disabled(disabled=True)

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

## 2. Run Level

```python
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key = ""

# Reference: https://ai.google.dev/gemini-api/docs/openai
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
    model_provider=external_client,
    tracing_disabled=True
)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant")

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print(result.final_output)
```

## 3. Global Level

```python
from agents import Agent, Runner, AsyncOpenAI, set_default_openai_client, set_tracing_disabled, set_default_openai_api

gemini_api_key = ""
set_tracing_disabled(True)
set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
set_default_openai_client(external_client)

agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model="gemini-2.0-flash")

result = Runner.run_sync(agent, "Hello")

print(result.final_output)
```

## How to Get Gemini API Key

Follow the instructions here to get your Gemini API Key:

### 🔗 [Get Gemini API Key](https://aistudio.google.com/welcome?utm_source=google&utm_medium=cpc&utm_campaign=FY25-global-DR-gsem-BKWS-1710442&utm_content=text-ad-none-any-DEV_c-CRE_736763307746-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt-AI%20Studio%20(Growth)-AI%20Studio-KWID_43700081658606392-aud-2301157399655:kwd-1276544732073&utm_term=KW_google%20ai%20studio-ST_google%20ai%20studio&gclsrc=aw.ds&gad_source=1&gad_campaignid=22301324850&gbraid=0AAAAACn9t67jh9G48BFOUsH68RSSsb-UI&gclid=CjwKCAjwwNbEBhBpEiwAFYLtGED3OBisW8C3wr_hAKn7r4d8y35pZddJJJxT8iv0QwvrVwpqTnZ7wxoCqMcQAvD_BwE)

### Installation

To install dependencies using uv:

```bash
uv add openai-agents python-dotenv
```

### Notes
- Agent Level configuration is best for when you need different models for different agents.
- Run Level is useful for changing the model per execution.
- Global Level sets a default model for your entire project.