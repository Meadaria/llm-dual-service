import asyncio
from celery import shared_task
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings
from app.services.openrouter_client import OpenRouterClient
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis


llm_client = OpenRouterClient()


def run_async(coro):
    """Безопасный запуск асинхронной функции в синхронном контексте."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None
    
    if loop and loop.is_running():
        # Если цикл уже запущен, создаём новый в отдельном потоке
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        # Если цикла нет, просто запускаем
        return asyncio.run(coro)


@shared_task(name="llm_request", bind=True)
def llm_request(self, tg_chat_id: int, prompt: str, user_token: str, system: str = None, temperature: float = 0.7):
    try:
        payload = decode_and_validate(user_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValueError("Invalid token payload: missing 'sub'")
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        answer = run_async(llm_client.chat_completion(messages=messages, temperature=temperature))
        
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        run_async(bot.send_message(chat_id=tg_chat_id, text=answer))
        run_async(bot.session.close())
        
        redis_client = get_redis()
        run_async(redis_client.lpush(f"chat_history:{user_id}", f"user: {prompt}\nassistant: {answer}"))
        
        return {"status": "success", "user_id": user_id, "answer": answer[:100]}
        
    except Exception as e:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        run_async(bot.send_message(chat_id=tg_chat_id, text=f"Ошибка: {str(e)}"))
        run_async(bot.session.close())
        
        raise self.retry(exc=e, countdown=60, max_retries=3)