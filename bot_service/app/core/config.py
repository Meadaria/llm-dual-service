from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "bot-service"
    ENV: str = "local"
    
    TELEGRAM_BOT_TOKEN: str
    
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: Optional[str] = None
    OPENROUTER_APP_NAME: Optional[str] = None
    
    # Прокси для Telegram
    PROXY_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()