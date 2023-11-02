from pydantic import BaseModel, EmailStr
from typing import Optional

# 기본 스키마
class UserBase(BaseModel):
  username: str
  nickname: str
  email: Optional[EmailStr] = None
  class Config:
    from_attributes = True
    
# 사용자 스키마
class UserCreate(UserBase):
  password: str
  
class User(UserBase):
  id: int