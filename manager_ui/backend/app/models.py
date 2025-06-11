from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
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

    shops = relationship(
        "BusinessAccount",
        secondary="manager_shops",
        back_populates="managers",
    )


class Message(Base):
    """Сообщение между пользователем и менеджером."""

    __tablename__ = "messages"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    role: str = Column(String, default="user")
    content: str = Column(Text, nullable=False)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")


class IntegrationType(str, Enum):
    """Типы интеграции магазина."""

    OZON = "ozon"
    WILDBERRIES = "wildberries"
    YAMARKET = "yamarket"
    AVITO = "avito"
    JIVO = "jivo"
    WEBSITE = "website"


class DataType(str, Enum):
    """Типы данных магазина."""

    TEXT = "text"
    WEB_PAGE = "web_page"
    DOCUMENT = "document"


manager_shops = Table(
    "manager_shops",
    Base.metadata,
    Column("manager_id", ForeignKey("users.id"), primary_key=True),
    Column("shop_id", ForeignKey("business_accounts.id"), primary_key=True),
)


class BusinessAccount(Base):
    """Магазин, к которому привязан менеджер.

    Помимо общей информации, хранит тип интеграции и API-ключ, необходимый
    для подключения к внешнему REST API магазина.
    """

    __tablename__ = "business_accounts"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    integration_type: IntegrationType = Column(SAEnum(IntegrationType), nullable=False)
    api_key: str | None = Column(String, nullable=True)
    creator_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    data_type: DataType = Column(SAEnum(DataType), nullable=True)
    data_content: str | None = Column(Text, nullable=True)

    creator = relationship("User", backref="created_shops")
    managers = relationship(
        "User",
        secondary=manager_shops,
        back_populates="shops",
    )
