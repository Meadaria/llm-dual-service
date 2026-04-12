from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings


#  строка подключения к SQLite
DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_PATH}"

#  асинхронный engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  
)

#  фабрика сессий
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Чтобы объекты не устаревали после коммита
)