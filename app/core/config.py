"""
Core configuration settings for AIRA application
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "sqlite:///./aira.db"
    
    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_number: str = "whatsapp:+14155552671"
    
    # API
    api_title: str = "AIRA - WhatsApp Parent Assistant"
    api_version: str = "1.0.0"
    debug: bool = True
    log_level: str = "INFO"
    
    # Session
    session_timeout: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get settings instance (cached)"""
    return Settings()
