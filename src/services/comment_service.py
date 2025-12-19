from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from fastapi import HTTPException

from src.models.comments import Comment
from src.services.article_service import ArticleService
from src.models.article import Article
#

class CommentService:

    @staticmethod
    async def get_by_id(comment_id: int, db: AsyncSession) -> Comment | None:
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalars().first()
    
    @staticmethod
    async def get_for_article(article_slug: str, db: AsyncSession):
        article = await ArticleService.get_article_by_slug(article_slug, db)
        if not article:
            return []
        result = await db.execute(
                select(Comment).where(Comment.article_id == article.id)
            )
        
        return result.scalars().all()
    
    @staticmethod
    async def create_comment(slug: str, content: str, user_id: int, db: AsyncSession) -> Comment:
        article = await ArticleService.get_article_by_slug(slug, db)
        comment = Comment(
            body=content,
            article_id=article.id,
            author_id=user_id,
        )

        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment

    @staticmethod
    async def delete_comment(comment_id: int, current_user_id: int, db: AsyncSession):
        comment = await CommentService.get_by_id(comment_id, db)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.author_id != current_user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

        await db.delete(comment)
        await db.commit()
