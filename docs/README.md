# Документация Manager UI

Этот сервис предоставляет REST API и веб-интерфейс для менеджеров, работающих с чатами пользователей. 
Используются Python 3.10, FastAPI и PostgreSQL. На фронтенде применён React.

## Быстрый старт

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Задайте переменную окружения `DATABASE_URL` с параметрами подключения к PostgreSQL и `TELEGRAM_BOT_TOKEN` для проверки авторизации.
3. Запустите сервер:
   ```bash
   uvicorn manager_ui.backend.app.main:app --reload
   ```
4. Откройте Swagger по адресу `http://localhost:8000/docs`.

Фронтенд расположен в каталоге `manager_ui/frontend` и может быть запущен любым сервером для статических файлов или инструментами сборки React.

## Запуск через Docker Compose

Для быстрого запуска всех сервисов можно воспользоваться `docker-compose`.
Убедитесь, что установлены Docker и Docker Compose, затем выполните:

```bash
docker-compose up --build
```

Приложение будет доступно по адресу `http://localhost:8000`, а фронтенд на `http://localhost:8080`.

## Основные возможности

- Авторизация через Telegram Mini App.
- Управление пользователями и сообщениями.
- Поддержка нескольких магазинов и привязки менеджеров к ним.
- WebSocket для мгновенного обмена сообщениями.

## Структура API

### Пользователи
- `POST /users/login` – авторизация пользователя Telegram.

### Сообщения
- `POST /messages/` – создать сообщение.
- `GET /messages/{user_id}` – получить историю сообщений пользователя.

### Магазины
- `POST /shops/` – создать магазин.
- `GET /shops/{shop_id}` – получить магазин.
- `PUT /shops/{shop_id}` – изменить магазин.
- `DELETE /shops/{shop_id}` – удалить магазин.
- `POST /shops/{shop_id}/managers/{manager_id}` – привязать менеджера.
- `DELETE /shops/{shop_id}/managers/{manager_id}` – отвязать менеджера.
- `GET /shops/{shop_id}/users` – список пользователей магазина и их ролей.

### WebSocket
WebSocket подключение осуществляется по адресу `/ws/{user_id}`. После подключения менеджер может получать и отправлять сообщения в режиме реального времени.

## Swagger
Документация API в формате Swagger доступна автоматически по адресу `/docs`, а в формате OpenAPI JSON – по `/openapi.json`.

