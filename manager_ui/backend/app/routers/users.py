"""Маршруты управления пользователями."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, crud, schemas
from ..db import get_session

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", response_model=schemas.UserRead)
async def login(data: schemas.UserCreate, db: AsyncSession = Depends(get_session)):
    """Авторизация пользователя через Telegram."""
    if not auth.verify_telegram_auth(data.dict()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth data")

    user = await crud.get_or_create_user(db, data)
    return user
