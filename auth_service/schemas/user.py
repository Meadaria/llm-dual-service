from pydantic import BaseModel


class UserPublic(BaseModel):
    """Публичная схема пользователя."""
    id: int
    email: str
    role: str
    created_at: datetime
    
    model_config = {"from_attributes": True}

