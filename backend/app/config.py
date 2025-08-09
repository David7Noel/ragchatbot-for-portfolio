import os # DIESE ZEILE HINZUFÜGEN!
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Dies setzt BASE_DIR auf das Stammverzeichnis deines Projekts
    # (z.B. C:\xampp\htdocs\meine_projekte\RAG-Chatbot_mit_Portfolio-Integration\)
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    HUGGINGFACEHUB_API_TOKEN: str = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
