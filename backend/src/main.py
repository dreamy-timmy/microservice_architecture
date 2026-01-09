from fastapi import FastAPI


from src.controllers.articles_controller import router as articles_router
from src.controllers.comments_controller import router as comments_router

app = FastAPI(title="Blog API")


app.include_router(articles_router)
app.include_router(comments_router)
