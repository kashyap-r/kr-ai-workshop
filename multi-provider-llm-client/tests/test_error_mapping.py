import httpx
from unittest.mock import patch

from groq import RateLimitError

from llm_client.config import load_config
from llm_client.errors import RateLimitError as LLMRateLimitError
from llm_client.groq_client import GroqClient


config = load_config()

client = GroqClient(
    api_key=config.groq_api_key,
    model=config.groq_model,
)


# Create a fake HTTP 429 response
mock_response = httpx.Response(
    status_code=429,
    request=httpx.Request(
        "POST",
        "https://api.groq.com/openai/v1/chat/completions",
    ),
)


# Create the actual Groq SDK exception
groq_error = RateLimitError(
    "Rate limit exceeded",
    response=mock_response,
    body={
        "error": {
            "message": "Rate limit exceeded"
        }
    },
)


with patch.object(
    client.client.chat.completions,
    "create",
    side_effect=groq_error,
):

    try:

        client.generate(
            "Tell me something fun."
        )

    except LLMRateLimitError as e:

        print("PASS")
        print(
            "Caught expected LLM RateLimitError:"
        )
        print(e)

    except Exception as e:

        print("FAIL")
        print(
            "Caught unexpected exception:"
        )
        print(
            f"{type(e).__name__}: {e}"
        )

    else:

        print("FAIL")
        print(
            "Expected RateLimitError "
            "was not raised."
        )