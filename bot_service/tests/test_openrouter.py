import pytest
import respx
from httpx import Response
from app.services.openrouter_client import OpenRouterClient
from app.core.config import settings


class TestOpenRouterClient:
    @pytest.mark.asyncio
    async def test_chat_completion_success(self):
        mock_response = {
            "choices": [
                {"message": {"content": "Привет! Это тестовый ответ от LLM."}}
            ]
        }
        
        async with respx.mock(base_url=settings.OPENROUTER_BASE_URL) as respx_mock:
            respx_mock.post("/chat/completions").mock(
                return_value=Response(200, json=mock_response)
            )
            
            client = OpenRouterClient()
            messages = [{"role": "user", "content": "Привет!"}]
            
            result = await client.chat_completion(messages)
            
            assert result == "Привет! Это тестовый ответ от LLM."
            assert len(respx_mock.calls) > 0

    @pytest.mark.asyncio
    async def test_chat_completion_handles_error(self):
        async with respx.mock(base_url=settings.OPENROUTER_BASE_URL) as respx_mock:
            respx_mock.post("/chat/completions").mock(
                return_value=Response(429, json={"error": "Rate limited"})
            )
            
            client = OpenRouterClient()
            messages = [{"role": "user", "content": "Привет!"}]
            
            with pytest.raises(Exception) as exc:
                await client.chat_completion(messages)
            
            assert "OpenRouter" in str(exc.value)