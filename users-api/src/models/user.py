from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.db.base import Base

class User(Base):
    '''
    User model representing users of the application.

    Parameters:
        id: Primary key for the user
        email: Unique email address of the user
        username: Unique username of the user
        hashed_password: Hashed password of the user
        bio: Short info about the user
        image_url: URL of the user image

    '''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
