import json
from functools import lru_cache
from typing import Annotated, List

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    app_name: str = "AI Marketing Post Generator API"
    app_env: str = "development"
    app_debug: bool = True
    backend_cors_origins: Annotated[List[str], NoDecode] = ["http://localhost:5173"]

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> List[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return []
            if stripped.startswith("["):
                parsed = json.loads(stripped)
                if not isinstance(parsed, list):
                    raise ValueError("backend_cors_origins JSON must be a list")
                return [str(item).strip() for item in parsed if str(item).strip()]
            return [origin.strip() for origin in stripped.split(",") if origin.strip()]
        return value

    database_url: str = "sqlite:///./ai_marketing.db"

    ai_provider: str = "openai"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-1.5-flash"

    @field_validator("ai_provider")
    @classmethod
    def validate_provider(cls, value: str) -> str:
        allowed = {"openai", "gemini"}
        if value not in allowed:
            raise ValueError(f"ai_provider must be one of {allowed}")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
