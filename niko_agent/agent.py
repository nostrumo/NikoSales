"""Бизнес-логика ответов агента."""

from __future__ import annotations

import logging
from typing import Iterable

from .openai_client import OpenAIClient
from .retriever import get_product_context
from .prompts import MANAGER_REFERRAL, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class SupportAgent:
    """Агент, отвечающий на вопросы клиентов."""

    def __init__(self, openai_client: OpenAIClient) -> None:
        """Сохраняет клиента OpenAI для последующих запросов."""
        self._client = openai_client

    async def answer_question(
        self, store_id: str, product_id: str, question: str
    ) -> str:
        """Отвечает на вопрос пользователя с учётом товарного контекста."""
        context = get_product_context(store_id, product_id)
        user_content = f"Контекст товара: {context}\nВопрос: {question}"
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]
        logger.debug("Отправляем запрос в OpenAI: %s", messages)
        answer = await self._client.ask(messages)
        if not _is_confident_answer(answer):
            return f"{answer}\n{MANAGER_REFERRAL}"
        return answer


def _is_confident_answer(answer: str) -> bool:
    """Простая эвристика, определяющая уверенность ответа."""
    negative_markers: Iterable[str] = ["не знаю", "затрудняюсь", "не уверен"]
    return not any(marker in answer.lower() for marker in negative_markers)
