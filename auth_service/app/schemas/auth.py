from pydantic import BaseModel, Field, EmailStr


class RegisterRequest(BaseModel):
    """Схема для регистрации нового пользователя."""
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(
        ..., 
        min_length=8,
        description="Пароль (минимум 8 символов)"
    )


class TokenResponse(BaseModel):
    """Схема ответа с токеном доступа."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Тип токена")