from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.deps import get_current_user

from src.db.session import get_db
from src.schemas.user import UserRead, UserUpdate
from src.schemas.subscription import SubscriptionKeySchema, SubscribeRequest

from src.services.subscription_service import SubscriptionService

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

@router.put('/users/me/subscription-key', response_model=UserRead)
async def set_subscription_key(
    data: SubscriptionKeySchema,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Установить subscription_key для текущего пользователя"""
    current_user.subscription_key = data.subscription_key
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.post("/users/subscribe", status_code=204)
async def subscribe(
    data: SubscribeRequest,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Подписать текущего пользователя на другого"""
    try:
        await SubscriptionService.subscribe(
            subscriber_id=current_user.id,
            author_id=data.target_user_id,
            db=db
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
