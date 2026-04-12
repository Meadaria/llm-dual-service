from passlib.context import CryptContext
from jose.exceptions import JWTError, ExpiredSignatureError
from jose import jwt
import time
from app.core.exceptions import InvalidTokenError, TokenExpiredError

from app.core.config import settings

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Превращает "сырой" пароль в безопасный хэш для хранения.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Проверяет, что введённый пароль соответствует сохранённому хэшу.
    """
    return pwd_context.verify(password, hashed_password)

def _now() -> int:
    """Возвращает текущее время в Unix timestamp"""
    return int(time.time())


def create_access_token(user_id: int, role: str = "user") -> str:
    """
    Создает JWT access token.
    """
    payload = {
        "sub": str(user_id),  # идентификатор пользователя
        "role": role,         # роль пользователя
        "type": "access",     # тип токена
        "iat": _now(),        # время выдачи
        "exp": _now() + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, 
        }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str):

    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALG]
        )
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise InvalidTokenError()
    
