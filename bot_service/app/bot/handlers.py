from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate, InvalidTokenError, TokenExpiredError
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()
redis_client = get_redis()


@router.message(Command("token"))
async def save_token(message: Message):
    parts = message.text.split()
    
    if len(parts) != 2:
        await message.answer(
            "Ошибка: укажите токен\n"
            "/token your_jwt_token\n\n"
            "Получить токен можно в Auth Service: /auth/login"
        )
        return
    
    token = parts[1]
    
    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise InvalidTokenError()
        
        await redis_client.set(f"tg_user:{message.from_user.id}", token)
        await redis_client.set(f"user:{user_id}:tg", message.from_user.id)
        
        await message.answer(
            f"Токен сохранён. Вы авторизованы как пользователь #{user_id}\n"
            f"Теперь вы можете отправлять сообщения для LLM."
        )
        
    except (InvalidTokenError, TokenExpiredError) as e:
        await message.answer(f"Ошибка: неверный токен - {str(e)}")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")


@router.message()
async def handle_message(message: Message):
    tg_user_id = message.from_user.id
    
    token = await redis_client.get(f"tg_user:{tg_user_id}")
    
    if not token:
        await message.answer(
            "Вы не авторизованы.\n"
            "Получите JWT токен в Auth Service и выполните команду:\n"
            "/token ваш_токен"
        )
        return
    
    # Декодируем bytes в строку, если Redis вернул bytes
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    
    try:
        payload = decode_and_validate(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise InvalidTokenError()
        
    except (InvalidTokenError, TokenExpiredError) as e:
        await message.answer(
            f"Токен недействителен: {str(e)}\n"
            f"Получите новый токен и выполните /token"
        )
        await redis_client.delete(f"tg_user:{tg_user_id}")
        return
    
    prompt = message.text
    
    # Отправляем задачу в RabbitMQ через Celery
    llm_request.delay(
        tg_chat_id=tg_user_id,
        prompt=prompt,
        user_token=token,
        system=None,
        temperature=0.7
    )
    
    await message.answer("Запрос принят, обрабатывается. Ответ придёт в этом чате.")