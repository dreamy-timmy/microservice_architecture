from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, future=True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, 
                                 expire_on_commit=False)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Dependency for FastAPI
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
