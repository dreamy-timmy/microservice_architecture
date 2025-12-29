from fastapi import FastAPI

from src.controllers.auth_controller import router as auth_router
from src.controllers.users_controller import router as user_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)

