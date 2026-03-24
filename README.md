# Project Management REST API

REST API сервис для управления проектами, задачами и исполнителями. Разработано в рамках учебного задания по курсу "Системный дизайн".

## Описание

Сервис предоставляет возможности для:
- Регистрации и аутентификации пользователей
- Создания и управления проектами
- Создания и отслеживания задач в проектах
- Поиска пользователей и проектов


## Установка и запуск

Перейдите в папку проекта.

Запустите контейнер:
```bash
docker-compose up --build
```
Откройте браузер и перейдите по адресу:
```
http://localhost:8000/docs
```


## API Endpoints

### Аутентификация

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | /api/auth/register | Регистрация нового пользователя | Нет |
| POST | /api/auth/login | Получение JWT токена | Нет |

### Пользователи

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | /api/users/search?login={login} | Поиск пользователя по логину | Нет |
| GET | /api/users/searchByName?pattern={pattern} | Поиск по маске имя и фамилия | Нет |

### Проекты

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | /api/projects | Создание проекта | Да |
| GET | /api/projects | Получение всех проектов | Нет |
| GET | /api/projects/search?name={name} | Поиск проекта по имени | Нет |

### Задачи

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| POST | /api/projects/{project_id}/tasks | Создание задачи в проекте | Да |
| GET | /api/projects/{project_id}/tasks | Получение всех задач проекта | Нет |
| GET | /api/tasks/{task_code} | Получение задачи по коду | Нет |

### Системные

| Метод | Endpoint | Описание | Авторизация |
|-------|----------|----------|-------------|
| GET | /health | Проверка работоспособности API | Нет |

## Примеры использования

### 1. Регистрация пользователя

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "login": "testuser",
    "password": "123456",
    "first_name": "Kos",
    "last_name": "Sm"
  }'
```

Ответ:
```json
{
  "id": 1,
  "login": "testuser",
  "first_name": "Kos",
  "last_name": "Sm",
  "created_at": "2026-03-24T16:32:05.467891"
}
```

### 2. Получение токена

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=123456"
```

Ответ:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Создание проекта (требуется авторизация)

```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Test project"
  }'
```

### 4. Создание задачи в проекте

```bash
curl -X POST http://localhost:8000/api/projects/1/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "First Task",
    "description": "Do something"
  }'
```

### 5. Получение задачи по коду

```bash
curl http://localhost:8000/api/tasks/TASK-1
```

Ответ:
```json
{
  "id": 1,
  "code": "TASK-1",
  "title": "First Task",
  "description": "Do something",
  "project_id": 1,
  "assignee_id": null,
  "status": "OPEN",
  "created_at": "2026-03-24T16:35:00.000000"
}
```
