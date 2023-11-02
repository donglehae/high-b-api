from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils

router = APIRouter(
  prefix="/user",
  tags=['User']
)

def duplicated_username(db: Session, username: str):
  return db.query(models.User).filter(models.User.username == username).first()

def duplicated_nickname(db: Session, nickname: str):
  return db.query(models.User).filter(models.User.nickname == nickname).first()

def raise_conflict(status_code: status, detail: str):
  raise HTTPException(status_code=status_code, detail=detail)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(request_data: schemas.UserCreate, db: Session = Depends(get_db)):
  """
  `회원 생성`
  """  
  if duplicated_username(db, request_data.username):
    raise_conflict(status.HTTP_409_CONFLICT, "이미 사용중인 아이디입니다.")
  if duplicated_nickname(db, request_data.nickname):
    raise_conflict(status.HTTP_409_CONFLICT, "이미 사용중인 닉네임입니다.")
  
  hashed_password = utils.hash(request_data.password)
  request_data.password = hashed_password
  new_user = models.User(**request_data.model_dump())
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  
  return new_user