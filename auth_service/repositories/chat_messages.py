from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.db.models import ChatMessageOrm


class ChatMessageRepository:
    
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessageOrm:
        """Добавить сообщение в историю."""
        message = ChatMessageOrm(
            user_id=user_id,
            role=role,
            content=content,
            created_at=date.today()
        )
        
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        
        return message
    
    async def get_recent_messages(self, user_id: int, limit: int = 10) -> list[ChatMessageOrm]:
        """Получить последние N сообщений пользователя."""
        query = (
            select(ChatMessageOrm)
            .where(ChatMessageOrm.user_id == user_id)
            .order_by(ChatMessageOrm.created_at.desc())
            .limit(limit)
        )
        result = await self._session.execute(query)
        messages = result.scalars().all()
        
        # в хронологическом порядке (от старых к новым)
        return list(reversed(messages))
    
    async def delete_user_history(self, user_id: int) -> None:
        """Удалить всю историю сообщений пользователя."""
        query = delete(ChatMessageOrm).where(ChatMessageOrm.user_id == user_id)
        await self._session.execute(query)
        await self._session.commit()