import pytest
from unittest.mock import AsyncMock, patch
from fakeredis.aioredis import FakeRedis


@pytest.fixture(autouse=True)
def mock_redis():
    """Мокает Redis для всех тестов."""
    fake_redis = FakeRedis()
    
    with patch("app.infra.redis.get_redis", return_value=fake_redis):
        with patch("app.bot.handlers.redis_client", fake_redis):
            yield fake_redis


@pytest.fixture
def mock_celery():
    """Мокает Celery задачу."""
    with patch("app.tasks.llm_tasks.llm_request.delay") as mock:
        yield mock


@pytest.fixture
def mock_jwt():
    """Мокает валидацию JWT."""
    with patch("app.core.jwt.decode_and_validate") as mock:
        mock.return_value = {"sub": "123"}
        yield mock