# hello people!!

this is a repo for OmSTU 7th term discipline **Microservice Architecture**...

### Microservice Architecture - Blog API

- **Production**: [https://your-app.com](https://your-app.com) _(добавить позже)_
- **Swagger UI (локально)**: http://localhost:3000/docs
- **ReDoc (локально)**: http://localhost:3000/redoc

## Быстрый старт

### Локальная разработка

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```
2. **Запустите только БД- Docker:**
```bash
docker-compose --profile dev up -d
```
3. **Запустите приложение:**
```bash
uvicorn src.main.app --reload
``` 

4. **Откройте Swagger UI:**
http://127.0.0.1:8000/docs

Here we go...

the suggested project scheme is:

```
├── src/                  # Исходный код
     ├── models/          # Слои работы с данными
     ├── routes/          # Объявление HTTP роутов
     └── controllers/     # Основная бизнес логика
├── migrations/           # Файлы миграций БД
├── .github/
│   └── workflows/        # GitHub Actions конфигурация
│       └── docker-publish.yaml
├── Dockerfile           # Dockerfile приложения
├── docker-compose.yaml   # Файл compose
├── .env.example         # Пример переменных окружения
└── README.md           # Документация проекта
```