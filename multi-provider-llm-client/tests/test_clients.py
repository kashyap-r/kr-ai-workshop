from llm_client.ollama_client import OllamaClient
from llm_client.gemini_client import GeminiClient
from llm_client.groq_client import GroqClient
from llm_client.config import load_config

config = load_config()

prompt = "Tell me something fun today"

ollama = OllamaClient(
    model=config.ollama_model
)

gemini = GeminiClient(
    api_key=config.gemini_api_key,
    model=config.gemini_model
)

groq = GroqClient(
    api_key=config.groq_api_key,
    model=config.groq_model
)

for name, client in [
    ("Ollama", ollama),
    ("Gemini", gemini),
    ("Groq", groq),
]:

    print(f"\n--- {name} ---")

    response = client.generate(prompt)

    print(response.text)
    print(f"Model: {response.model}")
    print(f"Latency: {response.latency_ms:.2f} ms")
    print(f"Input tokens: {response.input_tokens}")
    print(f"Output tokens: {response.output_tokens}")
    print(f"Total tokens: {response.total_tokens}")