from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    """Модель пользователя, авторизованного через Telegram."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    telegram_id: int = Column(Integer, unique=True, index=True, nullable=False)
    first_name: str | None = Column(String, nullable=True)
    last_name: str | None = Column(String, nullable=True)
    username: str | None = Column(String, nullable=True)

    messages = relationship("Message", back_populates="user")


class Message(Base):
    """Сообщение между пользователем и менеджером."""

    __tablename__ = "messages"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    role: str = Column(String, default="user")
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
