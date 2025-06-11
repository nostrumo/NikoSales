"""Функции доступа к данным."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from .prompts import generate_agent_prompt


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


async def create_business_account(
    db: AsyncSession, account_data: schemas.BusinessAccountCreate
) -> models.BusinessAccount:
    """Создаёт новый магазин.

    Параметры включают тип интеграции и, при необходимости, API‑ключ для
    взаимодействия с внешним REST API магазина.
    """
    account = models.BusinessAccount(**account_data.dict())
    account.agent_prompt = generate_agent_prompt(account)
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


async def add_manager_to_shop(
    db: AsyncSession, manager_id: int, shop_id: int
) -> None:
    """Привязывает менеджера к магазину."""
    manager = await db.get(models.User, manager_id)
    shop = await db.get(models.BusinessAccount, shop_id)
    if manager and shop and manager not in shop.managers:
        shop.managers.append(manager)
        await db.commit()


async def get_user_shops(db: AsyncSession, user_id: int) -> list[models.BusinessAccount]:
    """Возвращает список магазинов пользователя."""
    user = await db.get(models.User, user_id)
    return user.shops if user else []


async def get_shop(db: AsyncSession, shop_id: int) -> models.BusinessAccount | None:
    """Возвращает магазин по идентификатору."""
    return await db.get(models.BusinessAccount, shop_id)


async def update_business_account(
    db: AsyncSession, shop_id: int, data: schemas.BusinessAccountUpdate
) -> models.BusinessAccount | None:
    """Обновляет информацию о магазине."""
    shop = await db.get(models.BusinessAccount, shop_id)
    if not shop:
        return None

    for field, value in data.dict(exclude_unset=True).items():
        setattr(shop, field, value)

    shop.agent_prompt = generate_agent_prompt(shop)

    await db.commit()
    await db.refresh(shop)
    return shop


async def delete_business_account(db: AsyncSession, shop_id: int) -> None:
    """Удаляет магазин."""
    shop = await db.get(models.BusinessAccount, shop_id)
    if shop:
        await db.delete(shop)
        await db.commit()


async def remove_manager_from_shop(
    db: AsyncSession, manager_id: int, shop_id: int
) -> None:
    """Отвязывает менеджера от магазина."""
    shop = await db.get(models.BusinessAccount, shop_id)
    manager = await db.get(models.User, manager_id)
    if shop and manager and manager in shop.managers:
        shop.managers.remove(manager)
        await db.commit()


async def get_shop_users(db: AsyncSession, shop_id: int) -> list[tuple[models.User, str]]:
    """Возвращает пользователей магазина с указанием их ролей."""
    shop = await db.get(models.BusinessAccount, shop_id)
    if not shop:
        return []

    users: list[tuple[models.User, str]] = []
    if shop.creator:
        users.append((shop.creator, "creator"))

    for manager in shop.managers:
        users.append((manager, "manager"))

    return users
