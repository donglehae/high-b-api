from fastapi import APIRouter, UploadFile, status, Depends, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas, utils, oauth2

router = APIRouter(
  prefix="/hospital",
  tags=['Hospital']
)

def duplicated_name(db: Session, name: str):
  return db.query(models.Hospital).filter(models.Hospital.name == name).first()

def raise_conflict(status_code: status, detail: str):
  raise HTTPException(status_code=status_code, detail=detail)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.HospitalDetail)
def create_hospital(request_data: schemas.HospitalCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  """
  `병원 생성`
  """  
  if duplicated_name(db, request_data.name): raise_conflict(status.HTTP_409_CONFLICT, "이미 사용중인 병원명입니다.")

  new_business_hour = models.BusinessHour()
  db.add(new_business_hour)
  db.commit()
  db.refresh(new_business_hour)
  
  request_data.business_hour = new_business_hour.id
  new_hospital = models.Hospital(**request_data.model_dump())
  db.add(new_hospital)
  db.commit()
  db.refresh(new_hospital)
  
  return new_hospital

@router.get("/list", status_code=status.HTTP_200_OK, response_model=list[schemas.HospitalDetail])
def read_hospital_list(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  """
  `병원 목록`
  """
  hospital_list = db.query(models.Hospital).all()

  return hospital_list

@router.get("/{hospital_id}", status_code=status.HTTP_200_OK, response_model=schemas.HospitalDetail)
def read_hospital(hospital_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  """
  `병원 정보`
  """
  hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
  
  return hospital

@router.put("/{hospital_id}/image", status_code=status.HTTP_200_OK, response_model=schemas.Hospital)
def upload_hospital_image(hospital_id: int, image: UploadFile = File(...), db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  """
  `병원 대표이미지 추가`
  """  
  try:
    hospital_query = db.query(models.Hospital).filter(models.Hospital.id == hospital_id)
    if hospital_query.first() is None: raise_conflict(status.HTTP_404_NOT_FOUND, "존재하지 않는 병원입니다.")
    
    file_location = f"static/img/hospital/{hospital_id}.{image.filename.split('.')[-1]}"
    with open(file_location, "wb") as file: file.write(image.file.read())

    hospital_query.update({'image': file_location}, synchronize_session="evaluate")
    db.commit()
    return hospital_query.first()
  
  except Exception:
    raise_conflict(status.HTTP_400_BAD_REQUEST, "파일 업로드 실패")
  
@router.put("/{hospital_id}/hour", status_code=status.HTTP_200_OK, response_model=schemas.HospitalDetail)
def updatae_hospital_hour(hospital_id: int, request_data: schemas.BusinessHour, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
  """
  `병원 영업시간 수정`
  """  
  hospital = db.query(models.Hospital).filter(models.Hospital.id == hospital_id).first()
  business_hour_query = db.query(models.BusinessHour).filter(models.BusinessHour.id == hospital.business_hour)
  business_hour_query.update(request_data.model_dump(), synchronize_session="evaluate")
  db.commit()
  
  return hospital