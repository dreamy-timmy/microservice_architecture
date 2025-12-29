from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.deps import get_current_user

from src.db.session import get_db
from src.schemas.user import UserRead, UserUpdate


router = APIRouter(prefix="/api/users", tags=["users"])

@router.get('/user', response_model=UserRead)
async def get_user(current_user = Depends(get_current_user)):
    return UserRead.from_orm(current_user)

@router.put('/user', response_model=UserRead)
async def update_user(update_data: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    update_dict = update_data.dict(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(current_user, field, value)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return current_user



