from llm_client.config import load_config
from llm_client.errors import (
    ModelNotFoundError,
    LLMError,
)
from llm_client.groq_client import GroqClient


config = load_config()


client = GroqClient(
    api_key=config.groq_api_key,
    model="this-model-does-not-exist",
)


try:

    client.generate(
        "Tell me something fun."
    )

except ModelNotFoundError as e:

    print("PASS")
    print(
        f"Caught expected ModelNotFoundError: {e}"
    )

except LLMError as e:

    print("FAIL")
    print(
        "Caught an LLMError, but not "
        f"ModelNotFoundError: {type(e).__name__}"
    )

else:

    print("FAIL")
    print(
        "Expected ModelNotFoundError "
        "was not raised."
    )