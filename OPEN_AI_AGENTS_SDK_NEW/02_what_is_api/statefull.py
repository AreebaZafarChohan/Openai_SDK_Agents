# from openai import OpenAI
# import os

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# client = OpenAI(api_key=OPENAI_API_KEY)

# response = client.chat.completions.create(
#     model="gpt-4-vision-preview",
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "I am areeba zafar."},
#                 {
#                     "type": "text",
#                     "text": "I am areeba zafar."
#                 }
#             ]
#         }
#     ]
# )

# print(response.choices[0].message.content)

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY) # type: ignore

# Choose the model (Stateful chat supported models)
model = genai.GenerativeModel("gemini-1.5-flash")  # type: ignore 

# Create a stateful chat session
chat = model.start_chat(history=[])

# First message
response1 = chat.send_message("I am Areeba Zafar.")
print("Bot:", response1.text)

# Second message continues the same conversation
response2 = chat.send_message("What is my name?")
print("Bot:", response2.text)

# Third message (still remembers context)
response3 = chat.send_message("Now tell me something about yourself.")
print("Bot:", response3.text)
