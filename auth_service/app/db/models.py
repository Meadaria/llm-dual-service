from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import date


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str]
    role: Mapped[str]
    created_at: Mapped[date]

    chat_messages: Mapped[list["ChatMessageOrm"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class ChatMessageOrm(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    role: Mapped[str]
    content: Mapped[str]
    created_at: Mapped[date]

    user: Mapped["UsersOrm"] = relationship(back_populates="chat_messages")