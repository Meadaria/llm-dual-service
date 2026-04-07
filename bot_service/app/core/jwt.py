from jose import JWTError, ExpiredSignatureError
from jose import jwt
from typing import Dict, Any

from app.core.config import settings


class InvalidTokenError(Exception):
    """Токен невалидный."""
    pass


class TokenExpiredError(Exception):
    """Токен истёк."""
    pass


def decode_and_validate(token: str) -> Dict[str, Any]:
    """
    Проверяет JWT токен: подпись и срок действия.
    """
    # Удаляет префикс "Bearer " если есть
    if token.startswith("Bearer "):
        token = token[7:]
    
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