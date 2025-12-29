from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from src.db.session import get_db
from src.schemas.user import UserCreate, UserRead
from src.models.user import User
from src.services.auth_service import create_access_token, authenticate_user
from src.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=['auth'])

@router.post('/register', response_model=UserRead)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    '''
    Register the user with the given info
    
    '''
    user = await UserService.create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        bio=user_data.bio,
        img_url=user_data.image_url,
        db=db
    )
    return user
    
    
@router.post("/login", response_model=UserRead)
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    #finish that!
    user = await authenticate_user(user_data.email, user_data.password, db) 

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"id": user.id})
    
    return UserRead(email=user.email, username=user.username, token=token)


