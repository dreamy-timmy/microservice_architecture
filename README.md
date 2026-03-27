# hello people!!

this is a repo for OmSTU 7th term discipline **Microservice Architecture**...

### Microservice Architecture - Blog API

- **Production**: [https://microservice-architecture-latest.onrender.com/docs](https://microservice-architecture-latest.onrender.com/docs) 
- **Swagger UI (Posts API локально)**: http://localhost:8000/docs
- **Swagger UI (Users API локально)**: http://localhost:8001/docs
- **ReDoc (локально)**: http://localhost:3000/redoc

## Быстрый старт

### Локальная разработка (Docker Compose)

1. **Скопируйте .env:**
```bash
cp .env.example .env
```

2. **Запустите все сервисы через Docker Compose:**
```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (2 инстанса)
- Redis
- Backend API (порт 8000)
- Users API (порт 8001)
- Worker (обработка задач)
- Nginx Gateway (порт 80)

3. **Откройте Swagger UI:**
   - Backend: http://localhost:8000/docs
   - Users API: http://localhost:8001/docs

### Локальная разработка (без Docker - для разработки)

1. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

2. **Установите зависимости:**
```bash
cd backend
pip install -r requirements.txt

cd ../users-api
pip install -r requirements.txt

cd ../worker
pip install -r requirements.txt
```

3. **Запустите PostgreSQL и Redis локально:**
```bash
docker-compose -f docker-compose.dev.yml up -d
```

4. **Запустите миграции:**
```bash
cd backend
alembic upgrade head

cd ../users-api
alembic upgrade head
```

5. **Запустите приложения в разных терминалах:**

Terminal 1 - Backend:
```bash

├── backend/                  # API постов/комментариев
│   ├── src/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── celery.py    # Celery конфигурация
│   │   │   └── deps.py
│   │   ├── controllers/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── tasks.py         # Celery tasks
│   ├── migrations/
│   └── Dockerfile
│
├── users-api/                # Users API
│   ├── src/
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   └── subscription.py  # Модель подписок
│   │   ├── schemas/
│   │   │   └── subscription.py
│   │   ├── services/
│   │   │   └── subscription_service.py
│   │   ├── controllers/
│   │   │   └── users_controller.py
│   │   └── core/
│   ├── alembic/
│   │   └── versions/
│   │       └── 002_add_subscriptions.py
│   └── Dockerfile
│
├── worker/                   # Celery Worker
│   ├── worker.py            # Основная логика worker'a
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yaml      # Оркестрация всех сервисов
├── nginx.conf              # Конфигурация API Gateway
├── .env.example            # Пример переменных окружения
└── README.md

```

Here we go...