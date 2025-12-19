from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User
from src.core.security import hash_password

class UserService:

    @staticmethod
    async def get_by_id(user_id: int, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_by_email(user_email: str, db: AsyncSession) -> User | None:
        result = await db.execute(select(User).where(User.email == user_email))
        return result.scalars().first()

    @staticmethod
    async def create_user(email: str, username: str, password: str, bio: str, img_url: str, db: AsyncSession) -> User:
        hashed = hash_password(password)

        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed,
            bio=bio,
            image_url=img_url
        )

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user)

        return new_user
    
    @staticmethod
    async def update_user(user: User, data: dict, db: AsyncSession) -> User:
        for field, value in data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        # db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    @staticmethod
    async def delete_user(user: User, db: AsyncSession):
        await db.delete(user)
        await db.commit()
    


