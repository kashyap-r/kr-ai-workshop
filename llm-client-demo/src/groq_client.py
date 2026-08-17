import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

client = Groq(api_key=api_key)

response = client.chat.completions.create(
    model="llama-prompt-guard-2-86m",
    messages=[
        {
            "role": "user",
            "content": "Tell me something fun today"
        }
    ]
)

print(response.choices[0].message.content)