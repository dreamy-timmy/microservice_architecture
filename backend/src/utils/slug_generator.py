from fastapi import Depends
from sqlalchemy import select
from src.db.session import get_db
from src.models.article import Article
from sqlalchemy.ext.asyncio import AsyncSession

from slugify import slugify

async def generate_slug(title: str, db: AsyncSession) -> str:
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    
    while True:
        result = await db.execute(select(Article).where(Article.slug == slug))
        exists = result.scalar_one_or_none()

        if not exists:
            return slug
        
        slug = f"{base_slug}-{counter}"
        
        counter += 1

