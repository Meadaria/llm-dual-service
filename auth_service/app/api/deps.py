from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.core.security import decode_token
from app.core.exceptions import UserNotFoundError, InvalidTokenError, TokenExpiredError
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_db() -> AsyncSession:
    """Получение сессии базы данных."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Получение репозитория пользователей."""
    return UserRepository(db)


async def get_auth_usecase(
    user_repo: UserRepository = Depends(get_user_repo)
) -> AuthUseCase:
    """Получение usecase аутентификации."""
    return AuthUseCase(user_repo)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme)
) -> int:
    """Получение ID текущего пользователя из JWT."""
    try:
        payload = decode_token(token)
    except (InvalidTokenError, TokenExpiredError) as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return int(user_id)


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    user_repo: UserRepository = Depends(get_user_repo)
):
    """Получение текущего пользователя"""
    try:
        user = await user_repo.get_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )