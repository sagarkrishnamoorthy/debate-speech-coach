"""Configuration management for the Speech Analyzer application."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignore extra fields in .env
    )
    
    # Environment
    environment: str = "development"
    
    # API Keys
    gemini_api_key: str = ""
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # AI Provider
    default_ai_provider: Literal["gemini", "openai", "anthropic"] = "gemini"
    
    # AI Models - Single source of truth for model names
    gemini_model: str = "gemini-2.5-flash-lite"
    openai_model: str = "gpt-4-turbo-preview"
    anthropic_model: str = "claude-3-opus-20240229"
    
    # Audio Configuration
    max_audio_duration_seconds: int = 600
    sample_rate: int = 16000
    
    # Paths
    upload_dir: Path = Path("uploads")
    log_dir: Path = Path("logs")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        self.upload_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()
