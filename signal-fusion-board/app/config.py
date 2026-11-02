from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "OptiToken"
    APP_ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    CACHE_TTL_SECONDS: int = 86400

    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None

    DEFAULT_FAST_MODEL: str = "groq/llama-3.1-8b-instant"
    DEFAULT_BALANCED_MODEL: str = "gemini/gemini-1.5-flash"
    DEFAULT_REASONING_MODEL: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
