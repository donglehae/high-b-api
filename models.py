from sqlalchemy import TIMESTAMP, Column, String, text
from sqlalchemy.dialects.mysql import INTEGER
from database import Base

class User(Base):
  __tablename__ = "user"
  __table_args__ = {'comment': '사용자'}
  
  id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False, comment='사용자 PK')
  username = Column(String(50), nullable=False, unique=True, comment='아이디')
  nickname = Column(String(50), nullable=False, unique=True, comment='닉네임')
  password = Column(String(255), nullable=False, comment='비밀번호')
  email = Column(String(50), nullable=True, comment='이메일')
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), comment='생성 일시')
  last_login_at = Column(TIMESTAMP(timezone=True), nullable=True, comment='마지막 로그인 일시')
  deactivated_at = Column(TIMESTAMP(timezone=True), nullable=True, comment='비활성화 일시')