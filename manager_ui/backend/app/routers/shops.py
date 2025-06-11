"""Маршруты управления магазинами."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas
from ..db import get_session


router = APIRouter(prefix="/shops", tags=["shops"])


@router.post("/", response_model=schemas.BusinessAccountRead)
async def create_shop(
    account: schemas.BusinessAccountCreate, db: AsyncSession = Depends(get_session)
) -> schemas.BusinessAccountRead:
    """Создаёт магазин."""
    return await crud.create_business_account(db, account)


@router.post("/{shop_id}/managers/{manager_id}")
async def add_manager(
    shop_id: int, manager_id: int, db: AsyncSession = Depends(get_session)
) -> None:
    """Привязывает менеджера к магазину."""
    await crud.add_manager_to_shop(db, manager_id, shop_id)


@router.get("/by-user/{user_id}", response_model=list[schemas.BusinessAccountRead])
async def get_user_shops(user_id: int, db: AsyncSession = Depends(get_session)):
    """Возвращает магазины, привязанные к пользователю."""
    return await crud.get_user_shops(db, user_id)

