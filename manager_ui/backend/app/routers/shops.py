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


@router.put("/{shop_id}", response_model=schemas.BusinessAccountRead)
async def update_shop(
    shop_id: int,
    data: schemas.BusinessAccountUpdate,
    db: AsyncSession = Depends(get_session),
) -> schemas.BusinessAccountRead | None:
    """Редактирует информацию о магазине."""
    return await crud.update_business_account(db, shop_id, data)


@router.delete("/{shop_id}")
async def delete_shop(shop_id: int, db: AsyncSession = Depends(get_session)) -> None:
    """Удаляет магазин."""
    await crud.delete_business_account(db, shop_id)


@router.delete("/{shop_id}/managers/{manager_id}")
async def remove_manager(
    shop_id: int, manager_id: int, db: AsyncSession = Depends(get_session)
) -> None:
    """Отвязывает менеджера от магазина."""
    await crud.remove_manager_from_shop(db, manager_id, shop_id)


@router.get("/{shop_id}/users", response_model=list[schemas.ShopUser])
async def get_shop_users(shop_id: int, db: AsyncSession = Depends(get_session)):
    """Возвращает пользователей магазина и их роли."""
    pairs = await crud.get_shop_users(db, shop_id)
    return [
        schemas.ShopUser(
            id=user.id,
            telegram_id=user.telegram_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            role=role,
        )
        for user, role in pairs
    ]

