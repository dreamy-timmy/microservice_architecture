from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings

security = HTTPBearer()

async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload.get("id")
    
    except JWSError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://users-api:3000/auth/login") # tokenUrl="/users/login" localhost:8001

# def get_current_user_id(token: str = Depends(security)) -> int:
#     try:
#         payload = jwt.decode(
#             token,
#             settings.JWT_SECRET,
#             algorithms=[settings.JWT_ALGORITHM]
#         )
#         return payload.get("id")
#     except JWSError:
#         raise HTTPException(status_code=401, detail="Invalid token")







#     user = await db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")    

#     return user
