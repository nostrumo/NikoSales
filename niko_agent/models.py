"""Pydantic модели запросов и ответов."""

from __future__ import annotations

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Модель запроса от пользователя."""

    store_id: str
    product_id: str
    question: str


class AnswerResponse(BaseModel):
    """Модель ответа агента."""

    answer: str
