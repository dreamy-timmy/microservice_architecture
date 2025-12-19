from pydantic import BaseModel

class CommentIn(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    body: str
    author_id: int

    class Config:
        orm_mode = True

