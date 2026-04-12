import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import Message, User


@pytest.fixture
def fake_redis():
    from fakeredis.aioredis import FakeRedis
    redis = FakeRedis()
    with patch("app.bot.handlers.redis_client", redis):
        yield redis


@pytest.fixture
def mock_celery():
    with patch("app.tasks.llm_tasks.llm_request.delay") as mock:
        yield mock


@pytest.fixture
def fake_message():
    message = AsyncMock(spec=Message)
    message.from_user = User(id=123456, is_bot=False, first_name="Test")
    message.text = ""
    message.answer = AsyncMock()
    return message