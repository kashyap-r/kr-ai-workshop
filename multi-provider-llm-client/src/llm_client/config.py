"""
Author: Kashyap R
Date: 18th Aug, 2026
"""

import os 
from dataclasses import dataclass 
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

@dataclass
class LLMConfig:
    # provider: str = os.environ.get("LLM_PROVIDER", "ollama")
    # ollama_model: str = os.environ.get("OLLAMA_MODEL", "qwen3:8b")
    # gemini_api_key: str = os.environ.get("GEMINI_API_KEY", "")
    # gemini_model: str = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
    # groq_api_key: str = os.environ.get("GROQ_API_KEY", "")
    # groq_model: str = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")

    provider: str
    ollama_model: str
    gemini_api_key: str | None
    gemini_model: str
    groq_api_key: str | None
    groq_model: str

def load_config() -> LLMConfig:
    return LLMConfig(
        provider=os.getenv("LLM_PROVIDER", "ollama"),
        ollama_model=os.getenv("OLLAMA_MODEL", "qwen3:8b"),
        gemini_api_key=os.getenv("GEMINI_API_KEY"),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),    
    )

# Pending: So later we'll add configuration validation and safe logging.
