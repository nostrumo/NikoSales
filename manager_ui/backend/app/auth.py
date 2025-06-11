"""Модуль верификации авторизации через Telegram Mini App."""

import hashlib
import hmac
import os
from typing import Any


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")


def verify_telegram_auth(data: dict[str, Any]) -> bool:
    """Проверяет подлинность данных, полученных из Telegram."""
    if not BOT_TOKEN:
        return False

    auth_data = data.copy()
    check_hash = auth_data.pop("hash", "")
    data_check = [f"{k}={v}" for k, v in sorted(auth_data.items())]
    data_check_string = "\n".join(data_check)

    secret_key = hashlib.sha256(BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_hash == check_hash
