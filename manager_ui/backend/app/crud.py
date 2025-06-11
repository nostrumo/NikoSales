"""Функции доступа к данным."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def get_or_create_user(db: AsyncSession, user_data: schemas.UserCreate) -> models.User:
    """Возвращает существующего или создаёт нового пользователя."""
    stmt = select(models.User).where(models.User.telegram_id == user_data.telegram_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user:
        return user

    user = models.User(**user_data.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_message(db: AsyncSession, message_data: schemas.MessageCreate) -> models.Message:
    """Создаёт новое сообщение."""
    message = models.Message(**message_data.dict())
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message


async def get_user_messages(db: AsyncSession, user_id: int) -> list[models.Message]:
    """Возвращает список сообщений пользователя."""
    stmt = select(models.Message).where(models.Message.user_id == user_id).order_by(models.Message.created_at)
    result = await db.execute(stmt)
    return result.scalars().all()
