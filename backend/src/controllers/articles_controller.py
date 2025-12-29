from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_current_user_id
from src.db.session import get_db
from src.schemas.article import ArticleIn, ArticleOut, ArticleUpdate
from src.services.article_service import ArticleService


router = APIRouter(prefix="/api/articles")

@router.post('/', response_model=ArticleOut, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleIn,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
    ):
    '''
    Create a new article
        
    :param article_data: Description
    :type article_data: ArticleIn
    :param db: Description
    :type db: AsyncSession
    :param current_user: Description
    '''

    article = await ArticleService.create_article(
        title=article_data.title,
        description=article_data.description,
        content=article_data.body,
        author_id=user_id,
        db=db,
        tag_list=article_data.tag_list
    )
    return article

@router.get("/{slug}", response_model=ArticleOut)
async def get_article(slug: str, db: AsyncSession = Depends(get_db)):
    '''
    Retrieve article by slug
    '''
    article = await ArticleService.get_article_by_slug(slug, db)
    if not article:
        raise HTTPException(status_code=404, detail="Article was not found")
    return article

@router.put("/{slug}", response_model=ArticleOut)
async def update_article(
    slug: str,
    article_change_data: ArticleUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    '''
    Update existing article
    
    :param slug: some human understandable id
    :type slug: str
    :param article_change_data: Description
    :type article_change_data: dict
    :param db: Description
    :type db: AsyncSession
    :param current_user: Description
    :type current_user: User
    '''

    update_dict = article_change_data.dict(exclude_unset=True)

    article = await ArticleService.update_article(
            slug=slug,
            update_data=update_dict,
            user_id=user_id,
            db=db
        )
    return article

@router.delete('/{slug}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    slug: str, 
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await ArticleService.delete_article(
        slug=slug,
        user_id=user_id,
        db=db
    )
