from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class UserCreate(BaseModel):  
    email: EmailStr
    username: str
    password: str
    bio: Optional[str] = None
    image_url: Optional[str] = None

class UserRead(BaseModel):
    '''
    Parameters:
        email: 
        username: 
    '''
    email: EmailStr
    username: str
    bio: Optional[str] = None
    image_url: Optional[str] = None
    token: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None

    class Config:
        pass

