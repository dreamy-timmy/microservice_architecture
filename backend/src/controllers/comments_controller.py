from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_current_user
from src.db.session import get_db
from src.schemas.comments import CommentIn, CommentOut
from src.services.comment_service import CommentService

router = APIRouter(prefix='/api/articles/{slug}/comments')

@router.post("", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
async def add_comment(
    slug: str, 
    comment_data: CommentIn, 
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user)):
    """
    Add a new comment to article
    
    :param slug: Description
    :type slug: str
    :param comment_data: Description
    :type comment_data: CommentIn
    :param db: Description
    :type db: AsyncSession
    :param current_user: Description
    """    
    comment = await CommentService.create_comment(
        slug=slug,
        content=comment_data.body,
        user_id=current_user.id,
        db=db
    )
    return comment

@router.get("", response_model=list[CommentOut])
async def get_comments(slug: str, db: AsyncSession = Depends(get_db)):
    """
    Get comments for article
    
    :param slug: Description
    :type slug: str
    :param db: Description
    :type db: AsyncSession
    """
    comments = await CommentService.get_for_article(slug, db)

    return comments

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(slug: str, comment_id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Delete comment by id
    
    :param slug: Description
    :type slug: str
    :param comment_id: Description
    :type comment_id: int
    :param db: Description
    :type db: AsyncSession
    """
    await CommentService.delete_comment(comment_id, current_user.id, db)
