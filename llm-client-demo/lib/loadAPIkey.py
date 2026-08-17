
import os
from pathlib import Path
from dotenv import load_dotenv


def load_API_key_from_env():
    """
    Load the API key from the .env file located in the parent directory of the current working directory.
    Returns:
        str: The API key if found, otherwise raises an exception.
    """
    project_root = Path.cwd()
    env_file = project_root.parent / ".env"

    if not env_file.exists():
        raise FileNotFoundError("No .env file found in the parent directory.")

    load_dotenv(env_file)
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in the .env file.")

    return api_key

loaded_api_key = load_API_key_from_env()
print ("API key loaded:", bool(loaded_api_key))

