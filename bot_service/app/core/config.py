from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Настройки приложения
    APP_NAME: str = "bot-service"
    ENV: str = "local"
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN: str
    
    # JWT (для валидации токенов)
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    
    # Redis и RabbitMQ
    REDIS_URL: str = "redis://redis:6379/0"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672//"
    
    # OpenRouter
    OPENROUTER_API_KEY: Optional[str] = None
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "stepfun/step-3.5-flash:free"
    OPENROUTER_SITE_URL: Optional[str] = None
    OPENROUTER_APP_NAME: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()