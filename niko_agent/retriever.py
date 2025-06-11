"""Модуль для получения контекста по товару из разных магазинов."""

from __future__ import annotations

from typing import Dict


STORE_PRODUCTS: Dict[str, Dict[str, str]] = {
    "ozon": {
        "1": "Смартфон XYZ с отличной камерой и ёмкой батареей.",
        "2": "Ноутбук ABC для работы и развлечений.",
    },
    "wildberries": {
        "1": "Кроссовки Runner 3000, удобные и лёгкие.",
        "2": "Куртка зимняя WarmUp с утеплителем.",
    },
    "yamarket": {
        "1": "Телевизор UltraHD с поддержкой Smart TV.",
        "2": "Стиральная машина CleanWash с функцией быстрой стирки.",
    },
}


def get_product_context(store_id: str, product_id: str) -> str:
    """Возвращает описание товара для указанного магазина и идентификатора."""
    store = STORE_PRODUCTS.get(store_id.lower())
    if not store:
        return ""
    return store.get(product_id, "")
