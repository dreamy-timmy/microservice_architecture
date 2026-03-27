from fastapi import FastAPI

# Import Celery to initialize it
from src.core.celery import celery_app  # noqa
import src.tasks  # noqa - Register all tasks

from src.controllers.articles_controller import router as articles_router
from src.controllers.comments_controller import router as comments_router

app = FastAPI(title="Blog API")


app.include_router(articles_router)
app.include_router(comments_router)
