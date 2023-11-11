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
    
class BusinessHourBase(BaseModel):
  mon: Optional[str] = None
  tue: Optional[str] = None
  wed: Optional[str] = None
  thu: Optional[str] = None
  fri: Optional[str] = None
  sat: Optional[str] = None
  sun: Optional[str] = None
  class Config:
    from_attributes = True

class HospitalBase(BaseModel):
  name: str
  address: str
  introduction: Optional[str] = None
  class Config:
    from_attributes = True
    
# 사용자 스키마
class UserCreate(UserBase):
  password: str
  
class User(UserBase):
  id: int
  
# 영업시간 스키마
class BusinessHour(BusinessHourBase):
  pass
  
# 병원 스키마
class HospitalCreate(HospitalBase):
  business_hour: Optional[int] = None
  pass

class Hospital(HospitalBase):
  id: int
  image: Optional[str] = None
  rating: float

class HospitalDetail(Hospital):
  business_hour_info: Optional[BusinessHour] = None