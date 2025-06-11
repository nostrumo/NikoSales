"""Точка входа в приложение FastAPI."""

from fastapi import FastAPI

from .routers import chat, messages, users, shops

app = FastAPI(title="Manager UI")

app.include_router(users.router)
app.include_router(messages.router)
app.include_router(chat.router)
app.include_router(shops.router)
