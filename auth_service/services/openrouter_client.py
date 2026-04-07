import httpx
from typing import List, Dict

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    """Клиент для работы с OpenRouter API."""
    
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.referer = settings.OPENROUTER_SITE_URL
        self.title = settings.OPENROUTER_APP_NAME 
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        if self.referer:
            self.headers["HTTP-Referer"] = self.referer
        if self.title:
            self.headers["X-Title"] = self.title
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Запрос к OpenRouter и получение ответа модели.
        """
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
                    raise ExternalServiceError(
                        "OpenRouter",
                        response.status_code,
                        response.text
                    )
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
                
            except httpx.TimeoutException:
                raise ExternalServiceError(
                    "OpenRouter",
                    None,
                    "Request timeout"
                )
            except httpx.RequestError as e:
                raise ExternalServiceError(
                    "OpenRouter",
                    None,
                    str(e)
                )