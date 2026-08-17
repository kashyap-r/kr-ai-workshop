import os
from pathlib import Path 
from dotenv import load_dotenv

from llm_client.ollama_client import OllamaClient
from llm_client.gemini_client import GeminiClient
from llm_client.groq_client import GroqClient

# This step ensures where ever you run this script from .. the paths will be automatically resolved
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

prompt = "Tell me something fun today"
ollama = OllamaClient(
    model="qwen3:8b"
)

gemini = GeminiClient(
    api_key=os.environ["GEMINI_API_KEY"],
    model="gemini-3.5-flash"
)

# groq = GroqClient(
#     api_key=os.environ["GROQ_API_KEY"],
#     model="Qwen/Qwen3.6-27B"
# )
print("\n--- Ollama ---")
print(ollama.generate(prompt))

print("\n--- Gemini ---")
print(gemini.generate(prompt))

# print("\n--- Groq ---")
# print(groq.generate(prompt))