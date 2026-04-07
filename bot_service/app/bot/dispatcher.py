from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.core.config import settings
from app.bot.handlers import start_handler, message_handler


def create_bot() -> Bot:
    """Создаёт экземпляр бота."""
    return Bot(token=settings.TELEGRAM_BOT_TOKEN, parse_mode=ParseMode.HTML)


def create_dispatcher() -> Dispatcher:
    """Создаёт диспетчер и регистрирует обработчики."""
    dp = Dispatcher()
    
    # Регистрация роутеров и хендлеров
    dp.include_router(start_handler.router)
    dp.include_router(message_handler.router)
    
    return dp


# Глобальные экземпляры
bot = create_bot()
dp = create_dispatcher()