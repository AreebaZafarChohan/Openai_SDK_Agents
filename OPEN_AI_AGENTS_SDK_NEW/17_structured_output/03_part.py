from typing import List, Optional
from pydantic import BaseModel
from agents import Agent, Runner
import rich
from config import config

class ActionItem(BaseModel):
    task: str
    assignee: str
    # due_date: str | None = None
    due_date: str  = ""
    priority: str = "medium"

class Decision(BaseModel):
    topic: str
    decision: str
    # rationale: str | None = None
    rationale: str  = ""

class MeetingMinutes(BaseModel):
    meeting_title: str
    date: str
    attendees: list[str]
    agenda_items: list[str]
    key_decisions: list[Decision]
    action_items: list[ActionItem]
    # next_meeting_date: str | None = None
    next_meeting_date: str  = ""
    meeting_duration_minutes: int

# Meeting minutes extractor
agent = Agent(
    name="MeetingSecretary",
    instructions="""Extract structured meeting minutes from meeting transcripts.
    Identify all key decisions, action items, and important details.""",
    output_type=MeetingMinutes
)

meeting_transcript = """
Marketing Strategy Meeting - January 15, 2024
Attendees: Sarah (Marketing Manager), John (Product Manager), Lisa (Designer), Mike (Developer)
Duration: 90 minutes

Agenda:
1. Q1 Campaign Review
2. New Product Launch Strategy  
3. Budget Allocation
4. Social Media Strategy

Key Decisions:
- Approved $50K budget for Q1 digital campaigns based on strong ROI data
- Decided to launch new product in March instead of February for better market timing
- Will focus social media efforts on Instagram and TikTok for younger demographics

Action Items:
- Sarah to create campaign timeline by January 20th (high priority)
- John to finalize product features by January 25th
- Lisa to design landing page mockups by January 22nd
- Mike to review technical requirements by January 30th

Next meeting: January 29, 2024
"""

result = Runner.run_sync(agent, meeting_transcript, run_config=config)

print("=== Meeting Minutes ===")
rich.print(f"Meeting Minutes: {result.final_output}")