"""Точка входа для запуска веб-сервиса агента."""

from __future__ import annotations

import logging
import uvicorn
from fastapi import FastAPI

from niko_agent.agent import SupportAgent
from niko_agent.models import AnswerResponse, QuestionRequest
from niko_agent.openai_client import OpenAIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Niko Sales Agent")

client = OpenAIClient()
agent = SupportAgent(client)


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """HTTP endpoint для получения ответа от агента."""
    answer = await agent.answer_question(
        request.store_id, request.product_id, request.question
    )
    return AnswerResponse(answer=answer)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

