from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from database import get_db
from config import settings
import schemas, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def raise_conflict(status_code: status, detail: str, headers: Optional[dict]):
  raise HTTPException(status_code=status_code, detail=detail, headers=headers)

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
  return encoded_jwt

def verify_access_token(token: str, credentials_exception):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: int = payload.get("user_id")
    if user_id is None: raise credentials_exception
    return schemas.TokenData(id=user_id)
  except JWTError: raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="자격 증명을 검증할 수 없습니다.", headers={"WWW-Authenticate": "Bearer"})
  token_data = verify_access_token(token, credentials_exception)
  user = db.query(models.User).filter(models.User.id == token_data.id).first()
  if user is None: raise credentials_exception
  return user