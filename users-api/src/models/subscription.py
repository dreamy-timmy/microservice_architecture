from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.db.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    subscriber_id = Column(BigInteger, nullable=False, index=True)  # кто подписался
    author_id = Column(BigInteger, nullable=False, index=True)      # на кого подписались
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Уникальный индекс для предотвращения дублей
    __table_args__ = (
        UniqueConstraint('subscriber_id', 'author_id', name='uq_subscription'),
    )

