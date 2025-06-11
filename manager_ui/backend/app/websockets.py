"""Управление WebSocket-подключениями."""

from collections.abc import AsyncIterator
from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    """Простой менеджер WebSocket-подключений."""

    def __init__(self) -> None:
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int) -> None:
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: int, message: str) -> None:
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for websocket in self.active_connections.values():
            await websocket.send_text(message)


manager = ConnectionManager()
