import asyncio
from config import config
from agents import Agent, Runner
from agents.run import AgentRunner, set_default_agent_runner


class CustomRunner(AgentRunner):
    async def run(self, starting_agent, input, **kwargs):
        print("CustomRunner: Starting custom run...")
        # input = await self.preprocess(input)
        
        
        result = await super().run(starting_agent, input, **kwargs)
        
        # Custom postprocessing & analytics
        # await self.log_analytics(result)
        return result
    
set_default_agent_runner(CustomRunner())

async def main():
    # This agent will use the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
        run_config=config
    )
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())   