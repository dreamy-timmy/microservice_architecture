from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ArticleIn(BaseModel):
    title: str
    description: str
    body: str
    tag_list: Optional[list[str]] = Field(default_factory=list)
    
class ArticleOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str
    body: str
    tag_list: Optional[list[str]] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime
    favorited: bool = False
    favorites_count: int = 0
    
    class Config:
        orm_mode = True

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None

    class Config:
        orm_mode = True

