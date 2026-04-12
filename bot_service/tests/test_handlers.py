from jose import jwt
from app.bot.handlers import save_token, handle_message
from app.core.config import settings


class TestTokenHandler:
    async def test_save_token_success(self, fake_redis, fake_message):
        payload = {"sub": "123"}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        
        fake_message.text = f"/token {token}"
        
        await save_token(fake_message)
        
        saved_token = await fake_redis.get(f"tg_user:{fake_message.from_user.id}")
        if isinstance(saved_token, bytes):
            saved_token = saved_token.decode('utf-8')
        assert saved_token == token

    async def test_save_token_invalid_returns_error(self, fake_redis, fake_message):
        fake_message.text = "/token invalid.token.here"
        
        await save_token(fake_message)
        
        saved_token = await fake_redis.get(f"tg_user:{fake_message.from_user.id}")
        assert saved_token is None
        fake_message.answer.assert_called_once()
        assert "Ошибка" in fake_message.answer.call_args[0][0]

    async def test_handle_message_no_token(self, fake_redis, fake_message, mock_celery):
        fake_message.text = "Hello world"
        
        await handle_message(fake_message)
        
        mock_celery.assert_not_called()
        fake_message.answer.assert_called_once()
        assert "не авторизованы" in fake_message.answer.call_args[0][0]

    async def test_handle_message_with_token_sends_to_celery(self, fake_redis, fake_message, mock_celery):
        payload = {"sub": "123"}
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
        await fake_redis.set(f"tg_user:{fake_message.from_user.id}", token)
        
        fake_message.text = "Привет, как дела?"
        
        await handle_message(fake_message)
        
        mock_celery.assert_called_once()
        args, kwargs = mock_celery.call_args
        assert kwargs["tg_chat_id"] == fake_message.from_user.id
        assert kwargs["prompt"] == "Привет, как дела?"
        assert kwargs["user_token"] == token
        
        fake_message.answer.assert_called_once()
        assert "принят" in fake_message.answer.call_args[0][0]