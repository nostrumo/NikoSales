"""Маршруты для работы с сообщениями."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..db import get_session

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=schemas.MessageRead)
async def create_message(message: schemas.MessageCreate, db: AsyncSession = Depends(get_session)):
    """Создаёт сообщение пользователя."""
    return await crud.create_message(db, message)


@router.get("/{user_id}", response_model=list[schemas.MessageRead])
async def get_user_messages(user_id: int, db: AsyncSession = Depends(get_session)):
    """Возвращает историю сообщений пользователя."""
    return await crud.get_user_messages(db, user_id)
