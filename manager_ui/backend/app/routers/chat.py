"""WebSocket-чат с пользователем."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ..websockets import manager

router = APIRouter()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """Обрабатывает WebSocket-соединения."""
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
