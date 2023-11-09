from fastapi import FastAPI, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pytz import timezone
from datetime import datetime
from database import get_db
from routers import user, hospital
import schemas, models, utils, oauth2
import uvicorn

app = FastAPI()

routers = [user.router, hospital.router]
for router in routers: app.include_router(router)

def raise_conflict(status_code: status, detail: str):
  raise HTTPException(status_code=status_code, detail=detail)

@app.post('/login', response_model=schemas.Token, tags=["Login"])
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  """
  `로그인`
  """
  user_query = db.query(models.User).filter(models.User.username == user_credentials.username)
  user = user_query.first()
  
  if not user or not utils.verify(user_credentials.password, user.password):
    raise_conflict(status.HTTP_401_UNAUTHORIZED, "로그인에 실패하였습니다.")
  
  access_token = oauth2.create_access_token(data={"user_id": user.id})
  user_query.update({"last_login_at": datetime.now(timezone('Asia/Seoul'))}, synchronize_session="evaluate")
  db.commit()
  
  return {"access_token": access_token, "token_type": "bearer"}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=30180)