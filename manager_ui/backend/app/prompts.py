"""Генерация промтов для ИИ-агента."""

from . import models


def generate_agent_prompt(account: models.BusinessAccount) -> str:
    """Формирует промт для ИИ на основе информации о магазине."""
    parts: list[str] = []
    if account.data_content:
        parts.append(account.data_content)
    if account.shipping_info:
        parts.append(f"Доставка: {account.shipping_info}")
    if account.location_info:
        parts.append(f"Местоположение: {account.location_info}")
    if account.ai_topics:
        parts.append(f"ИИ отвечает на: {account.ai_topics}")
    if account.manager_topics:
        parts.append(f"Менеджер отвечает на: {account.manager_topics}")
    return "\n".join(parts)
