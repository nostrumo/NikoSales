from datetime import datetime
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
