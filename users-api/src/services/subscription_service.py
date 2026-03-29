from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.subscription import Subscription
from src.models.user import User

class SubscriptionService:

    @staticmethod
    async def subscribe(subscriber_id: int, target_username: str, db: AsyncSession) -> Subscription:
        """Подписатьcя на другого пользователя

        Parameters:
            subscriber_id: ID пользователя, который подписывается
            target_username: имя пользователя, на которого подписываются
            db: Асинхронная сессия базы данных
        """
        author_id = await db.execute(select(User.id).where(User.username == target_username))
        author_id = author_id.scalars().first()

        if not author_id:
            raise ValueError("User not found")

        if author_id == subscriber_id:
            raise ValueError("Cannot subscribe to yourself")

        # Проверяем, нет ли уже такой подписки
        existing = await db.execute(
            select(Subscription).where(
                and_(
                    Subscription.subscriber_id == subscriber_id,
                    Subscription.author_id == author_id
                )
            )
        )
        
        if existing.scalars().first():
            raise ValueError("Already subscribed")
        
        subscription = Subscription(
            subscriber_id=subscriber_id,
            author_id=author_id
        )
        db.add(subscription)
        await db.commit()
        await db.refresh(subscription)
        return subscription

    @staticmethod
    async def unsubscribe(subscriber_id: int, author_id: int, db: AsyncSession) -> bool:
        """Отписаться от пользователя"""
        result = await db.execute(
            select(Subscription).where(
                and_(
                    Subscription.subscriber_id == subscriber_id,
                    Subscription.author_id == author_id
                )
            )
        )
        subscription = result.scalars().first()
        if subscription:
            await db.delete(subscription)
            await db.commit()
            return True
        return False

    @staticmethod
    async def get_author_subscribers(author_id: int, db: AsyncSession) -> list[dict]:
        """Получить всех подписчиков автора"""
        result = await db.execute(
            select(User.id, User.username, User.subscription_key).join(
                Subscription,
                Subscription.subscriber_id == User.id
            ).where(Subscription.author_id == author_id)
        )
        subscribers = result.all()
        return [
            {"id": sub[0], "username": sub[1], "subscription_key": sub[2]}
            for sub in subscribers if sub[2]  # Фильтруем только тех, у кого есть ключ
        ]

    @staticmethod
    async def is_subscribed(subscriber_id: int, author_id: int, db: AsyncSession) -> bool:
        """Проверить подписку"""
        result = await db.execute(
            select(Subscription).where(
                and_(
                    Subscription.subscriber_id == subscriber_id,
                    Subscription.author_id == author_id
                )
            )
        )
        return result.scalars().first() is not None
