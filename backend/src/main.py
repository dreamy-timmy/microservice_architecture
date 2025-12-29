from fastapi import FastAPI

from src.controllers.auth_controller import router as auth_router
from src.controllers.users_controller import router as users_router
from src.controllers.articles_controller import router as articles_router
from src.controllers.comments_controller import router as comments_router

app = FastAPI(title="Blog API")

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(articles_router)
app.include_router(comments_router)
