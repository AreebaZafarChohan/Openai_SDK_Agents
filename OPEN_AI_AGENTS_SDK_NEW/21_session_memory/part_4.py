from agents import Agent, Runner, SQLiteSession
from config import config

class CustomerSupportBot:
    def __init__(self):
        self.agent = Agent(
            name="SupportBot",
            instructions="""You are a helpful customer support agent.
            Remember the customer's information and previous issues throughout the conversation.
            Be friendly and professional."""
        )

    def get_customer_session(self, customer_id: str):
        """Get or create a session for a specific customer"""
        return SQLiteSession(f"customer_{customer_id}", "support_conversations.db")

    def chat_with_customer(self, customer_id: str, message: str):
        """Handle a customer message"""
        session = self.get_customer_session(customer_id)

        result = Runner.run_sync(
            self.agent,
            message,
            session=session,
            run_config=config,
        )

        return result.final_output

# Example usage
support_bot = CustomerSupportBot()

# Customer 123's conversation
print("=== Customer 123 Support Session ===")
print("Customer: Hi, I'm having trouble with my order #12345")
response1 = support_bot.chat_with_customer("123", "Hi, I'm having trouble with my order #12345")
print(f"Support: {response1}")

print("\nCustomer: The item was damaged when it arrived")
response2 = support_bot.chat_with_customer("123", "The item was damaged when it arrived")
print(f"Support: {response2}")

print("\nCustomer: What was my order number again?")
response3 = support_bot.chat_with_customer("123", "What was my order number again?")
print(f"Support: {response3}")  # Should remember order #12345!

# Different customer's conversation
print("\n=== Customer 456 Support Session ===")
print("Customer: Hello, I need help with billing")
response4 = support_bot.chat_with_customer("456", "Hello, I need help with billing")
print(f"Support: {response4}")  # Fresh conversation, no memory of customer 123