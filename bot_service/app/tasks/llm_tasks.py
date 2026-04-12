import asyncio
from aiogram import Bot

from app.core.config import settings
from app.services.openrouter_client import OpenRouterClient
from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.infra.celery_app import celery_app

llm_client = OpenRouterClient()


@celery_app.task(name="llm_request", bind=True)
def llm_request(self, tg_chat_id: int, prompt: str, user_token: str, system: str = None, temperature: float = 0.7):
    """Celery задача для вызова LLM через OpenRouter."""
    try:
        payload = decode_and_validate(user_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise ValueError("Invalid token payload: missing 'sub'")
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        answer = asyncio.run(llm_client.chat_completion(messages=messages, temperature=temperature))
        
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=tg_chat_id, text=answer))
        asyncio.run(bot.session.close())
        
        redis_client = get_redis()
        asyncio.run(redis_client.lpush(f"chat_history:{user_id}", f"user: {prompt}\nassistant: {answer}"))
        
        return {"status": "success", "user_id": user_id, "answer": answer[:100]}
        
    except Exception as e:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=tg_chat_id, text=f"Ошибка: {str(e)}"))
        asyncio.run(bot.session.close())
        
        raise self.retry(exc=e, countdown=60, max_retries=3)