from config import config
import asyncio
from agents import Agent, MaxTurnsExceeded, RunContextWrapper, function_tool, StopAtTools, Runner
from pydantic import BaseModel

class UserContext(BaseModel):
    role: str

@function_tool
def get_user_data(user_id: str) -> str:
    """Looks up user data by user ID."""
    return f"Data for {user_id}: Name - Areeba Zafar, Role - user"

def is_user_admin(ctx: RunContextWrapper[UserContext], agent: Agent[UserContext]) -> bool:
    return ctx.context.role == "admin" if ctx.context else False


@function_tool(is_enabled=is_user_admin) # type: ignore
def delete_user(user_id: str) -> str:
    """[ADMIN ONLY] Deletes a user. This is a final action."""

    return f"User {user_id} has been deleted."

admin_agent = Agent(
    name="Admin Agent",
    instructions="Help manage users. First get data, then delete if asked.",
    tools=[get_user_data, delete_user],
    tool_use_behavior=StopAtTools(stop_at_tool_names=["delete_user"]),
)

async def main():
    print("--- Running as a regular user ---")
    try:
       
        result_user = await Runner.run(
            admin_agent,
            "Please delete user client_456.",
            context=UserContext(role="user"),
            max_turns=5,   # safety limit
            run_config=config
        )
        print(f"Final Output as User: {result_user.final_output}")
        
        result_admin = await Runner.run(
            admin_agent,
            "Please delete user client_456.",
            context=UserContext(role="admin"),
            max_turns=5,   # safety limit
            run_config=config
        )
        print(f"Final Output as Admin: {result_admin.final_output}")
    except MaxTurnsExceeded as e:
        print(f"Max Turns exceeded for admin run. Error: {str(e)}")
    except Exception as e:        
        print(f"Error in admin run. Error {str(e)}")
        
if __name__ == "__main__":
    asyncio.run(main())