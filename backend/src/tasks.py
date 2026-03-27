from src.core.celery import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def send_post_notification(self, author_id: int, post_id: int):
    """
    Отправить уведомления подписчикам о новом посте
    
    Эта задача ставится в очередь при публикации поста.
    Worker прочитает эту задачу из Redis и обработает её.
    """
    logger.info(f"Task queued: send notifications for post {post_id} by author {author_id}")
    # Задача просто ставится в очередь, обработкой займется worker
    return {
        "status": "queued",
        "author_id": author_id,
        "post_id": post_id
    }
