from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NNIA Backend"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # OpenAI
    OPENAI_API_KEY: str
    ASSISTANT_ID: str
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str
    
    # Environment
    ENVIRONMENT: str = "development"
    API_VERSION: str = "v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permitir campos extra

@lru_cache()
def get_settings() -> Settings:
    return Settings() 