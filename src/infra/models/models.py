from sqlalchemy import Column, Integer, String, ForeignKey, Boolean,func,DateTime,Float
from sqlalchemy.dialects.mysql import JSON
from src.infra.config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

#migrar no alembic - comando: alembic revision --autogenerate -m "mensagem"
#migrar no alembic - comando: alembic upgrade head


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    password = Column(String(255), nullable=False)
    token = Column(String(255), nullable=True)
    
    
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=False, nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(String(50), nullable=True)
    cnpj = Column(String(50), nullable=True)
    active = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())