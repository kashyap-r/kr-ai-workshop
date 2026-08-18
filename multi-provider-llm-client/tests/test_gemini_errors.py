from llm_client.errors import (
    AuthenticationError,
    LLMError,
)
from llm_client.gemini_client import GeminiClient


client = GeminiClient(
    api_key="deliberately-invalid-key",
    model="gemini-3.5-flash",
)


try:

    client.generate(
        "Tell me something fun."
    )

except AuthenticationError as e:

    print("PASS")
    print(
        f"Caught expected AuthenticationError: {e}"
    )

except LLMError as e:

    print("FAIL")
    print(
        "Caught an LLMError, but not "
        f"AuthenticationError: {type(e).__name__}"
    )

else:

    print("FAIL")
    print(
        "Expected AuthenticationError "
        "was not raised."
    )