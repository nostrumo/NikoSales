"""Клиент для обращения к OpenAI API."""

from __future__ import annotations

import os
from typing import Dict, List

import openai


class OpenAIClient:
    """Обёртка над API OpenAI для отправки запросов."""

    def __init__(self, api_key: str | None = None, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("API ключ OpenAI не задан")
        self.model = model
        openai.api_key = self.api_key

    async def ask(self, messages: List[Dict[str, str]]) -> str:
        """Отправляет список сообщений в OpenAI и возвращает ответ."""
        response = await openai.ChatCompletion.acreate(model=self.model, messages=messages)
        return response.choices[0].message.content
