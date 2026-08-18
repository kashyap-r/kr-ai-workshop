"""
Author: Kashyap R
Date: 18th Aug, 2026
"""

import os 
from dataclasses import dataclass 
from pathlib import Path
from dotenv import load_dotenv
from .retry import RetryPolicy

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

@dataclass
class LLMConfig:
    provider: str
    ollama_model: str
    gemini_api_key: str | None
    gemini_model: str
    groq_api_key: str | None
    groq_model: str
    timeout_seconds: float
    retry_policy: RetryPolicy

def load_config() -> LLMConfig:
    retry_policy = RetryPolicy(
    max_attempts=int(
        os.environ["LLM_MAX_ATTEMPTS"]
    ),

    initial_delay_seconds=float(
        os.environ["LLM_INITIAL_RETRY_DELAY"]
    ),

    max_delay_seconds=float(
        os.environ["LLM_MAX_RETRY_DELAY"]
    ),

    backoff_multiplier=float(
        os.environ["LLM_BACKOFF_MULTIPLIER"]
    ),

    jitter=os.environ[
        "LLM_RETRY_JITTER"
    ].lower() == "true",
)
    return LLMConfig(
        provider=os.getenv("LLM_PROVIDER"),

        ollama_model=os.environ["OLLAMA_MODEL"],
        gemini_model=os.environ["GEMINI_MODEL"],
        groq_model=os.environ["GROQ_MODEL"],

        gemini_api_key=os.environ.get("GEMINI_API_KEY"),
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        
        timeout_seconds=float(os.environ["LLM_TIMEOUT_SECONDS"]),
        
        retry_policy=retry_policy
    )
    

    # return LLMConfig(
    #     provider=os.getenv("LLM_PROVIDER", "ollama"),
    #     ollama_model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
    #     gemini_api_key=os.getenv("GEMINI_API_KEY"),
    #     gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
    #     groq_api_key=os.getenv("GROQ_API_KEY"),
    #     groq_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),    
    # )
# Warning: The model names here in the config are default names .i.e. it means Use GEMINI_MODEL from the environment if it exists; otherwise use gemini-3.5-flash from here. 
# Same for the other models. So if you want to use a different model, you can set it in the .env file or change the default here.    
