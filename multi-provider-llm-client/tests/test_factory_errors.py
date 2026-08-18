from llm_client.config import load_config
from llm_client.errors import (
    ProviderError,
)
from llm_client.factory import LLMFactory


config = load_config()


try:

    LLMFactory.create(
        "does-not-exist",
        config,
    )

except ProviderError as e:

    print("PASS")
    print(f"Caught expected ProviderError: {e}")

else:

    print("FAIL")
    print("Expected ProviderError was not raised.")