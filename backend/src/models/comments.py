from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.base import Base

class Comment(Base):
    """
    Comment model representing comments made by users on articles.

    Parameters:
        id: Primary key for the comment
        body: Text content of the comment
        article_id: Foreign key referencing the associated article
        author_id: Foreign key referencing the user who made the comment
        created_at: Timestamp of when the comment was created
   
    """
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    author_id = Column(Integer, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    article = relationship("Article", back_populates="comments")
    # author = relationship("User", back_populates="comments")
