"""
Celery worker для обработки задач фоновых уведомлений
"""
import os
import logging
from celery import Celery
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
DATABASE_URL_USERS = os.getenv(
    "DATABASE_URL_USERS",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/users_db"
)
PUSH_SERVICE_URL = os.getenv("PUSH_SERVICE_URL", "http://localhost:8000")

# Инициализация Celery
app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,  # Подтверждаем задачу только после успешного выполнения
    worker_prefetch_multiplier=1,  # Берем по одной задаче за раз
)

# Подготовка к работе с асинхронной БД
engine = create_async_engine(DATABASE_URL_USERS, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_notifications(self, author_id: int, post_id: int):
    """
    Обработать задачу отправки уведомлений о новом посте
    
    Args:
        author_id: ID автора поста
        post_id: ID поста
    """
    try:
        logger.info(f"Processing notification task: author_id={author_id}, post_id={post_id}")
        asyncio.run(_send_notifications_async(author_id, post_id))
        logger.info(f"Successfully processed notifications for post {post_id}")
        return {"status": "success", "post_id": post_id}
    except Exception as exc:
        logger.error(f"Error processing task: {exc}")
        # Повторяем с увеличивающимся интервалом
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


async def _send_notifications_async(author_id: int, post_id: int):
    """Асинхронная логика отправки уведомлений"""
    import httpx
    
    # Получаем подписчиков из User БД
    async with AsyncSessionLocal() as session:
        subscribers = await get_author_subscribers(session, author_id)
    
    if not subscribers:
        logger.info(f"No subscribers for author {author_id}")
        return
    
    logger.info(f"Found {len(subscribers)} subscribers for author {author_id}")
    
    # Подготавливаем сообщение
    post_title = f"Post {post_id}"  # В реальном приложении получали бы из БД
    message = f"User {author_id} published a new post: {post_title[:10]}..."
    
    # Отправляем уведомления параллельно
    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = [
            send_notification_to_subscriber(client, subscriber, message, author_id)
            for subscriber in subscribers
        ]
        await asyncio.gather(*tasks, return_exceptions=True)


async def send_notification_to_subscriber(client, subscriber, message, author_id):
    """Отправить уведомление конкретному подписчику"""
    import httpx
    
    subscription_key = subscriber.get("subscription_key")
    user_id = subscriber.get("id")
    
    if not subscription_key:
        logger.warning(f"User {user_id} has no subscription_key, skipping")
        return
    
    try:
        response = await client.post(
            f"{PUSH_SERVICE_URL}/api/v1/notify",
            headers={
                "Authorization": f"Bearer {subscription_key}",
                "Content-Type": "application/json",
            },
            json={"message": message},
        )
        response.raise_for_status()
        logger.info(f"Notification sent successfully to user {user_id}")
    except httpx.HTTPError as e:
        logger.warning(f"Failed to send notification to user {user_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error sending notification to user {user_id}: {e}")


async def get_author_subscribers(session: AsyncSession, author_id: int):
    """Получить всех подписчиков автора с их subscription_key"""
    from sqlalchemy import select
    
    # Строим запрос к таблицам users и subscriptions
    # SELECT u.id, u.subscription_key FROM users u
    # JOIN subscriptions s ON u.id = s.subscriber_id
    # WHERE s.author_id = ?
    
    # query = """
    # SELECT u.id, u.subscription_key 
    # FROM users u
    # JOIN subscriptions s ON u.id = s.subscriber_id
    # WHERE s.author_id = :author_id AND u.subscription_key IS NOT NULL
    # """
    
    result = await session.execute(
        select(
            "id",
            "subscription_key"
        ).select_from(
            "SELECT u.id, u.subscription_key FROM users u "
            "JOIN subscriptions s ON u.id = s.subscriber_id "
            "WHERE s.author_id = :author_id AND u.subscription_key IS NOT NULL"
        ),
    )
    
    # На самом деле для SQLAlchemy нужно правильно выстроить запрос
    # Давайте используем raw SQL через text()
    from sqlalchemy import text
    
    result = await session.execute(
        text(
            """
            SELECT u.id, u.subscription_key 
            FROM users u
            JOIN subscriptions s ON u.id = s.subscriber_id
            WHERE s.author_id = :author_id AND u.subscription_key IS NOT NULL
            """
        ),
        {"author_id": author_id}
    )
    
    rows = result.fetchall()
    return [
        {"id": row[0], "subscription_key": row[1]}
        for row in rows
    ]


@app.task(bind=True)
def health_check(self):
    """Проверка здоровья worker'а"""
    logger.info("Health check: worker is alive")
    return {"status": "healthy"}


if __name__ == "__main__":
    app.start()
