from sqlalchemy import ForeignKey, TIMESTAMP, Column, String, Text, text
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.mysql import INTEGER, FLOAT
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
  
class Category(Base):
  __tablename__ = "category"
  __table_args__ = {'comment': '수술 카테고리'}
  
  id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False, comment='카테고리 PK')
  name = Column(String(50), nullable=False, unique=True, comment='카테고리명')
  
class BusinessHour(Base):
  __tablename__ = "business_hour"
  __table_args__ = {'comment': '영업시간'}
  
  id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False, comment='영업시간 PK')
  mon = Column(String(50), nullable=True, comment='월요일')
  tue = Column(String(50), nullable=True, comment='화요일')
  wed = Column(String(50), nullable=True, comment='수요일')
  thu = Column(String(50), nullable=True, comment='목요일')
  fri = Column(String(50), nullable=True, comment='금요일')
  sat = Column(String(50), nullable=True, comment='토요일')
  sun = Column(String(50), nullable=True, comment='일요일')
  
class Hospital(Base):
  __tablename__ = "hospital"
  __table_args__ = {'comment': '병원'}
  
  id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False, comment='병원 PK')
  name = Column(String(50), nullable=False, comment='병원명')
  address = Column(String(50), nullable=False, comment='주소')
  introduction = Column(Text, nullable=True, comment='병원 소개글')
  image = Column(Text, nullable=True, comment='대표이미지')
  rating = Column(FLOAT, nullable=False, server_default=text('0'), comment='리뷰 평점')
  business_hour = Column(INTEGER(unsigned=True), ForeignKey("business_hour.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True, comment='영업시간 FK')
  
  business_hour_info = relationship("BusinessHour", lazy="joined")