# SHIFT TZ — Система бронирования переговорных комнат

REST API для управления переговорными комнатами, временными слотами и бронированиями.

## Функциональность

### Пользователи

* Регистрация пользователя
* Авторизация по JWT-токену
* Получение информации о пользователях

### Комнаты

* Создание комнаты (только администратор)
* Удаление комнаты (только администратор)
* Получение списка комнат

### Временные слоты

* Создание временных слотов для комнаты (только администратор)
* Проверка пересечения слотов

### Бронирования

* Создание бронирования
* Просмотр бронирований на выбранную дату
* Отмена бронирования
* Контроль доступа по ролям

### Доступность переговорных

* Получение списка комнат
* Просмотр свободных и занятых слотов на выбранную дату

---

# Технологии

* Python 3.13
* FastAPI
* SQLAlchemy 2.0
* PostgreSQL
* AsyncPG
* JWT
* Pydantic v2
* Poetry
* Docker
* Docker Compose

---

# Структура проекта

```text
core/
├── api/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── models/
├── config.py
└── database_helper.py

main.py
Dockerfile
docker-compose.yml
pyproject.toml
```

---

# Настройка окружения

Создать файл `.env`

```env
# Приложение
APP_CONFIG__HOST=0.0.0.0
APP_CONFIG__PORT=8000

# База данных
APP_CONFIG__DB__USERNAME=postgres
APP_CONFIG__DB__PASSWORD=postgres
APP_CONFIG__DB__HOST=postgres
APP_CONFIG__DB__PORT=5432
APP_CONFIG__DB__NAME=postgres
APP_CONFIG__DB__ECHO=false

# JWT
APP_CONFIG__TOKEN__SECRET_KEY=0123456789
```

---

# Запуск локально

## Установка зависимостей

```bash
poetry install
```

## Запуск PostgreSQL

Например через Docker:

```bash
docker run --name postgres ^
-e POSTGRES_USER=postgres ^
-e POSTGRES_PASSWORD=postgres ^
-e POSTGRES_DB=postgres ^
-p 5438:5432 ^
-d postgres:17-alpine
```

Для локального запуска необходимо изменить `.env`:

```env
APP_CONFIG__DB__HOST=localhost
APP_CONFIG__DB__PORT=5438
```

## Запуск приложения

```bash
poetry run uvicorn main:app --reload
```

или

```bash
python main.py
```

---

# Запуск через Docker

## Dockerfile

Приложение контейнеризировано и может запускаться вместе с PostgreSQL через Docker Compose.

## Сборка

```bash
docker compose build
```

## Запуск

```bash
docker compose up
```

или

```bash
docker compose up -d
```

---

# Docker Compose

```yaml
services:
  postgres:
    image: postgres:17-alpine
    container_name: postgres

    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres

    ports:
      - "5438:5432"

  app:
    build: .
    container_name: shift_app

    env_file:
      - .env

    depends_on:
      - postgres

    ports:
      - "8000:8000"
```

---

# Проверка запуска

После запуска Docker Compose:

```bash
docker ps
```

Ожидаемый результат:

```text
postgres
shift_app
```

Проверить логи:

```bash
docker compose logs -f
```

Ожидаемый вывод:

```text
INFO: Started server process
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

# Swagger документация

После запуска приложение доступно по адресу:

```text
http://localhost:8000/docs
```

OpenAPI схема:

```text
http://localhost:8000/openapi.json
```

---

# API Endpoints

## Пользователи

### Регистрация

```http
POST /api/users/
```

### Получить пользователя

```http
GET /api/users/{user_id}/
```

### Получить список пользователей

```http
GET /api/users/
```

---

## Авторизация

### Вход

```http
POST /api/auth/
```

### Текущий пользователь

```http
GET /api/auth/me
```

---

## Комнаты

### Получить список комнат

```http
GET /api/rooms/
```

### Создать комнату

```http
POST /api/rooms/
```

### Удалить комнату

```http
DELETE /api/rooms/{room_id}/
```

---

## Временные слоты

### Создать слот

```http
POST /api/rooms/{room_id}/time-slots/
```

---

## Бронирования

### Создать бронирование

```http
POST /api/reservations/
```

### Получить бронирования на дату

```http
GET /api/reservations/?date=YYYY-MM-DD
```

### Удалить бронирование

```http
DELETE /api/reservations/{reservation_id}/
```

---

## Доступность комнат

### Получить доступность на дату

```http
GET /api/rooms/availability/?date=YYYY-MM-DD
```

---

# Роли

## ADMIN

Может:

* создавать комнаты;
* удалять комнаты;
* создавать временные слоты;
* просматривать все бронирования;
* удалять любые бронирования.

## EMPLOYEE

Может:

* создавать бронирования;
* просматривать только свои бронирования;
* отменять только свои бронирования.

---

# Автор

Александр Редун
