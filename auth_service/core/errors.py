from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовое исключение для всех HTTP-ошибок Auth Service."""
    pass


class UserAlreadyExistsError(BaseHTTPException):
    """Пользователь с таким email уже существует (409)."""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{email}' already exists"
        )


class InvalidCredentialsError(BaseHTTPException):
    """Неверный email или пароль (401)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidTokenError(BaseHTTPException):
    """Невалидный токен (401)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class TokenExpiredError(BaseHTTPException):
    """Токен истёк (401)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserNotFoundError(BaseHTTPException):
    """Пользователь не найден (404)."""
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found"
        )


class PermissionDeniedError(BaseHTTPException):
    """Нет прав доступа (403)."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )