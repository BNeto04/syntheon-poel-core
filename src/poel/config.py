from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl


class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str
    POEL_MODEL: str = "gpt-4o"
    POEL_MAX_OUTPUT_TOKENS: int = 800
    POEL_WINDOW_TURNS: int = 12

    # Sechel Integration
    SECHEL_API_URL: HttpUrl = "http://localhost:8001"
    SECHEL_ENABLED: bool = False

    # Session Management
    SESSION_TTL_HOURS: int = 3
    SESSION_DIR: str = ".sessions"

    @property
    def SESSION_TTL(self) -> timedelta:
        return timedelta(hours=self.SESSION_TTL_HOURS)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
