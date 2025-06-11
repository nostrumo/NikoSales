from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None


class UserCreate(UserBase):
    """Схема создания пользователя."""

    pass


class UserRead(UserBase):
    """Схема чтения пользователя."""

    id: int

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    """Базовая схема сообщения."""

    user_id: int
    role: str
    content: str


class MessageCreate(MessageBase):
    """Схема создания сообщения."""

    pass


class MessageRead(MessageBase):
    """Схема чтения сообщения."""

    id: int
    created_at: datetime

    class Config:
        orm_mode = True


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


class BusinessAccountBase(BaseModel):
    """Базовая схема магазина.

    Содержит общие поля для описания магазина, включая тип интеграции и
    необязательный API-ключ для доступа к сторонним сервисам.
    """

    name: str
    integration_type: IntegrationType
    api_key: str | None = None
    data_type: DataType | None = None
    data_content: str | None = None


class BusinessAccountCreate(BusinessAccountBase):
    """Схема создания магазина."""

    creator_id: int


class BusinessAccountUpdate(BaseModel):
    """Схема обновления магазина."""

    name: str | None = None
    integration_type: IntegrationType | None = None
    api_key: str | None = None
    data_type: DataType | None = None
    data_content: str | None = None


class BusinessAccountRead(BusinessAccountBase):
    """Схема чтения магазина."""

    id: int
    creator_id: int

    class Config:
        orm_mode = True


class ShopUser(BaseModel):
    """Пользователь магазина с указанием его роли."""

    id: int
    telegram_id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    role: str

    class Config:
        orm_mode = True
