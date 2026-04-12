from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Настройки приложения
    APP_NAME: str = "auth-service"
    ENV: str = "local"
    
    # JWT настройки
    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # База данных
    SQLITE_PATH: str = "./auth.db"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()