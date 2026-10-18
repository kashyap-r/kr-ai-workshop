# Expose the function to the outside world
from .llm_utils import get_ai_response

# Optional: explicitly define what is allowed to be imported
__all__ = ["get_ai_response"]
