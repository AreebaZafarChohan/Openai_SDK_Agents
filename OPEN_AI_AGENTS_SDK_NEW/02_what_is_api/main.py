import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
client = OpenAI(
    api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Run Basic Chat Completion
def main():
    print("🧠 Asking Gemini a question...\n")
    
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user",   "content": "Explain how AI works in simple terms."},
        ]
    )
    
    message = response.choices[0].message.content
    print("💡 Gemini's Response:\n")
    print(message)
    
if __name__ == "__main__":
    main()    