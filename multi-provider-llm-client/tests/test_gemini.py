
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Find the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load this project's .env
load_dotenv(PROJECT_ROOT / ".env")

key = os.environ["GEMINI_API_KEY"]

print("Key found:", bool(key))
print("Key length:", len(key))
print("Key prefix:", key[:6] + "...")

client = genai.Client(api_key=key)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Say hello in one short sentence."
)

print(response.text)