from src.models.article import Article
from fastapi import HTTPException

def ensure_article_exists(article: Article, ):
    if not article:
        raise HTTPException(status_code=404, detail="Article was not found")
    return True

def ensure_article_owner(article: Article, user_id: int):
    if article.author_id != user_id:
        raise HTTPException(status_code=403, detail="You are not the author of the article")
    return True
