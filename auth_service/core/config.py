from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Обязательные поля с значениями по умолчанию или без
    APP_NAME: str 
    ENV: str
    
    # JWT настройки
    JWT_SECRET: str 
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    
    # База данных
    SQLITE_PATH: str 
    
    # OpenRouter настройки
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str 
    OPENROUTER_MODEL: str 
    OPENROUTER_SITE_URL: Optional[str] = None
    OPENROUTER_APP_NAME: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True 

settings = Settings()