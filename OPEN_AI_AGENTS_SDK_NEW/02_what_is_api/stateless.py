# import os , openai
# from dotenv import load_dotenv

# load_dotenv()

# gemini_api_key = os.getenv("GEMINI_API_KEY") 

# openai_api_key = os.getenv("OPENAI_API_KEY_1") 

# openai.api_key = openai_api_key

# response = openai.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say hello! I'm Areeba Zafar"}]
# )
# print(response.choices[0].message.content)

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=gemini_api_key) # type: ignore

# Choose model
model = genai.GenerativeModel("gemini-1.5-flash")  # ya "gemini-1.5-pro" # type: ignore

# Generate response
response = model.generate_content("Say hello! I'm Areeba Zafar")

# Print output
print("Stateless")
print(response.text)


response_2 = model.generate_content("What's my name?")

print(response_2.text)