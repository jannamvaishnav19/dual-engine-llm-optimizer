from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    api_key: str = ""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-20b"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"
    redis_url: str = ""
    cache_ttl_seconds: int = 3600
    provider_timeout_seconds: float = 45.0
    max_prompt_chars: int = 20000
    cors_origins: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def validate_deployment(self):
        if self.app_env == "production" and not self.api_key:
            raise RuntimeError("API_KEY must be configured in production")
        if self.app_env == "production" and not (self.gemini_api_key and self.groq_api_key):
            raise RuntimeError("Configure both GEMINI_API_KEY and GROQ_API_KEY for cloud dual-engine mode")

@lru_cache
def get_settings() -> Settings:
    return Settings()
