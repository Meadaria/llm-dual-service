import httpx
from typing import List, Dict

from app.core.config import settings


class OpenRouterClient:
    """Клиент для работы с OpenRouter API."""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if settings.OPENROUTER_SITE_URL:
            self.headers["HTTP-Referer"] = settings.OPENROUTER_SITE_URL
        if settings.OPENROUTER_APP_NAME:
            self.headers["X-Title"] = settings.OPENROUTER_APP_NAME
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Отправляет запрос к OpenRouter и возвращает ответ модели."""
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    headers=self.headers,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code != 200:
                    raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.TimeoutException:
                raise Exception("OpenRouter API timeout")
            except httpx.RequestError as e:
                raise Exception(f"OpenRouter request error: {str(e)}")