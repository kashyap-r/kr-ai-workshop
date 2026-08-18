from llm_client.config import load_config
from llm_client.factory import LLMFactory
from llm_client.errors import LLMError


config = load_config()

prompt = "Tell me something fun today"


for provider in ["ollama", "gemini", "groq"]:

    print(f"\n--- {provider.upper()} ---")

    try:

        client = LLMFactory.create(
            provider,
            config,
        )

        response = client.generate(prompt)

        print(response.text)
        print(f"Model: {response.model}")
        print(
            f"Latency: "
            f"{response.latency_ms:.2f} ms"
        )
        print(
            f"Input tokens: "
            f"{response.input_tokens}"
        )
        print(
            f"Output tokens: "
            f"{response.output_tokens}"
        )
        print(
            f"Total tokens: "
            f"{response.total_tokens}"
        )

    except LLMError as e:

        print(
            f"LLM request failed: {e}"
        )