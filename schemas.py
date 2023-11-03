from pydantic import BaseModel, EmailStr
from typing import Optional

class TokenData(BaseModel):
  id: Optional[int] = None

class Token(BaseModel):
  access_token: str
  token_type: str

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