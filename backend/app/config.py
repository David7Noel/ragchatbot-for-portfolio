import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# ❶ Basisverzeichnis für das Backend
BASE_DIR: Path = Path(__file__).parent.parent

class Settings(BaseSettings):
    BASE_DIR: Path = BASE_DIR
    HUGGINGFACEHUB_API_TOKEN: str | None = None
    # OpenAI wird nicht mehr verwendet, daher optional
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
