# import nest_asyncio  # type: ignore
# nest_asyncio.apply()

from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")
print("Loaded API Key:", OPENROUTER_API_KEY)

BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "deepseek/deepseek-chat-v3-0324:free"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": MODEL,
    "messages": [
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
}

response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, data=json.dumps(data))

print("Status Code:", response.status_code)
print("\n=============================================\n")
print("Raw Response:", response.text)
print("\n=============================================\n")


try:
    print("Parsed JSON:", response.json())
    print("\n=============================================\n")
except requests.exceptions.JSONDecodeError:
    print("❌ Invalid JSON response.")
