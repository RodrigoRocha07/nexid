from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,func,DateTime,Float
from sqlalchemy.dialects.mysql import JSON
from src.infra.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session



class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    password = Column(String(255), nullable=False)
