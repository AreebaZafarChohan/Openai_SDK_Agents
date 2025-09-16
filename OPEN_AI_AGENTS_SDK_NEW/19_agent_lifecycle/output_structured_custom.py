from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled,AgentOutputSchemaBase
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Any
import os
from pydantic_core import CoreSchema, core_schema


set_tracing_disabled(disabled=True)
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-1.5-flash"
)

class MovieReview(BaseModel):
    is_positive: bool
    genre: str
    summary: str

#---------------------------------------
class OutputSchema(AgentOutputSchemaBase):
    def is_plain_text(self) -> bool:
        return False

    def name(self) -> str:
        return "MovieReviews"
    
    def json_schema(self):
        # review = {
        #     'is_positive': True, 
        #     'genre': 'sci-fi', 
        #     'summary': 'A thrilling and exciting sci-fi blockbuster with edge-of-the-seat action scenes and a captivating plot.'
        # }
        # return review
        return MovieReview.model_json_schema()
    
    def is_strict_json_schema(self) -> bool:
        return True
    
    def validate_json(self, json_str: str) -> Any:
       return MovieReview.model_validate_json(json_str)
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> CoreSchema:
        # Delegate schema generation to MovieReview's schema
        return handler(MovieReview)
#---------------------------------------

agent = Agent(
    name="MovieAnalyzer",
    instructions="Analyze the movie review and determine if it's positive, identify the genre, and provide a brief summary. Include any additional details like sentiment score or related genres if relevant.",
    model=model,
    output_type=OutputSchema
)

result = Runner.run_sync(
    starting_agent=agent,
    input="I loved the thrilling action scenes in this sci-fi blockbuster! The plot kept me on edge.",
)

print(result.final_output)