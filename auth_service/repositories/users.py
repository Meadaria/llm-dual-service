from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.db.models import UsersOrm
from app.core.exceptions import UserNotFoundError


class UserRepository:
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def get_by_id(self, user_id: int) -> UsersOrm:
        """Получить пользователя по ID."""
        query = select(UsersOrm).where(UsersOrm.id == user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise UserNotFoundError(user_id)
        
        return user
    
    async def get_by_email(self, email: str) -> UsersOrm | None:
        """Получить пользователя по email."""
        query = select(UsersOrm).where(UsersOrm.email == email)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, email: str, password_hash: str, role: str = "user") -> UsersOrm:
        """Создать нового пользователя."""
        user = UsersOrm(
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=date.today()
        )
        
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        
        return user