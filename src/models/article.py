from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.base import Base


class Article(Base):
    """
    Docstring for Article

    Fields:
        id: (primary key)
        slug: (needs to be specified)
        title: (needs to be specified)
        description: (needs to be specified)
        body: (needs to be specified)
        tag_list:
        
    """
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)

    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False) 
    body = Column(Text, nullable=False)

    tag_list = Column(ARRAY(String), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")

