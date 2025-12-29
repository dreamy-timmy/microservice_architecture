from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.article import Article
from src.core.validators import ensure_article_exists, ensure_article_owner

from src.utils.slug_generator import generate_slug

class ArticleService:

    @staticmethod
    async def get_article_by_slug(article_slug: str, db: AsyncSession) -> Article | None:
        result = await db.execute(select(Article).where(Article.slug == article_slug))
        return result.scalars().first()

    @staticmethod
    async def get_all_articles(db: AsyncSession):
        result = await db.execute(select(Article))
        return result.scalars().all()
    
    @staticmethod
    async def create_article(
        title: str, 
        description: str, 
        content: str, 
        author_id: int, 
        db: AsyncSession, 
        tag_list: list[str]=None) -> Article:
            
            slug = await generate_slug(title, db)
            article = Article(
                title=title,
                slug=slug,                
                body=content,
                description=description,
                author_id=author_id,
                tag_list=tag_list
            )
            db.add(article)
            await db.commit()
            await db.refresh(article)
            return article
    
    @staticmethod
    async def update_article(slug: str, update_data: dict, user_id: int, db: AsyncSession) -> Article:
        result = await db.execute(
            select(Article).where(Article.slug == slug)
        )
        article = result.scalars().first()
        
        ensure_article_exists(article=article)
        ensure_article_owner(article=article, user_id=user_id)

        # define allowed-for-change field:
        allowed_fields = ['title', 'description', 'body']

        for field in allowed_fields:
            if field in update_data:
                setattr(article, field, update_data[field])

        if 'title' in update_data:
            article.slug = await generate_slug(update_data['title'], db)

        db.add(article)
        await db.commit()
        await db.refresh(article)
        
        return article

    
    @staticmethod
    async def delete_article(slug: str, user_id: int, db: AsyncSession):

        res = await db.execute(
            select(Article).where(Article.slug == slug)
        )
        article = res.scalars().first()

        ensure_article_exists(article=article)
        ensure_article_owner(article=article, user_id=user_id)

        await db.delete(article)
        await db.commit()
