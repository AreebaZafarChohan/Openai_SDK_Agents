# 1. pip install litellm / uv add litellm

# 2. Setting up environment variables
import os
from dotenv import load_dotenv
from litellm import completion, exceptions # type: ignore

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTROPIC_API_KEY")

if openai_key is None or anthropic_key is None:
    raise ValueError("Missing API key(s) in .env file.")

os.environ["OPENAI_API_KEY"] = openai_key
os.environ["ANTHROPIC_API_KEY"] = anthropic_key



# 3. Making a completion request
messages = [{"role": "user", "content": "Hello, how are you?"}]
response = completion(model="gpt-3.5-turbo", messages=messages)
print(response["choices"][0]["message"]["content"])

print("\n==========================\n")
# For Anthropic's Claude
response2 = completion(model="claude-2", messages=messages)
print(response2["choices"][0]["message"]["content"])

print("\n==========================\n")
# For VertexAI's Gemini
response3 = completion(model="claude-2", messages=messages)
print(response3["choices"][0]["message"]["content"])

# 4. Handling Streaming Response

print("\n==========================\n")

response4 = completion(model="gpt-3.5-turbo", messages=messages, stream=True)
for part in response4:
    print(part["choices"][0]["delta"].get('content', ""), end="")
    
# 5. Exception Handling 

from openai.error import OpenAIError # type: ignore

try:
    response = completion(model="claude-2", messages=messages)
except OpenAIError as e:
    print(f"An error occured: {e}")    
    
# 6. Logging and Observability

litellm.sucess_callback = ["lunary", "langfuse", "helicone"]     # type: ignore

# Fakkback Example

def anthropic():
    try:
        print("Attempting to use anthropic model")
        response = completion(
            model = "claude-3-5-sonnet-20241022",
            messages=[{"content": "Hello, how are you?", "role": "user"}]
        )
    except exceptions.BadRequestError as e:
        print(f"\n!!!!!!!!!!! E R R O R !!!!!!!!!!!!!!!!!!!!!!!")
        print(f"---ERROR DETAIL --- {e}\n")
        print("\n!!!!!!!!!!!! Attempting to use gemini model !!!!!!!!!!!!!!!!!!!\n")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{ "content": "Hello, how are you?","role": "user"}]
            )
        print(response)    