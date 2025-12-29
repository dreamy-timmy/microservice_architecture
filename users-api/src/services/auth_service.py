from datetime import datetime, timedelta
from jose import jwt, JWSError
from passlib.context import CryptContext
from src.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta 
        else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    
    return encoded

def decode_access_token(token: str) -> dict:
    '''
    Decodes and verifies a JWT access token.
    '''
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWSError:
        return None
    
async def authenticate_user(user_email: str, plain_password: str, db: AsyncSession):
    '''
    Authenticate registered user

    Parameters:
        email: User email
        plain_password: Raw password provided by user
        db: Current session
    '''
    result = await db.execute(
        select(User).where(User.email == user_email)
    )

    user = result.scalars().first()

    if not user: 
        return None
    
    if not verify_password(plain_password, user.hashed_password): 
        return None
    
    return user
