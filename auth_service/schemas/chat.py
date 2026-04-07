from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Схема запроса к чату"""
    prompt: str = Field(..., description="Основной текст запроса пользователя")
    system: Optional[str] = Field(
        default=None, 
        description="Системная инструкция для модели"
    )
    max_history: Optional[int] = Field(
        default=10, 
        ge=1, 
        le=50,
        description="Количество последних сообщений из истории (от 1 до 50)"
    )
    temperature: Optional[float] = Field(
        default=0.7, 
        ge=0.0, 
        le=2.0,
        description="Креативность модели"
    )


class ChatResponse(BaseModel):
    """Схема ответа чата"""
    answer: str = Field(..., description="Ответ модели")
    
    model_config = {"from_attributes": True}