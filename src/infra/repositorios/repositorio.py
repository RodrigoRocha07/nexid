from src.infra.config.database import criar_db, get_db
from src.infra.models import models
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.providers.token_provider import *
from typing import Dict
from fastapi import HTTPException
#__________________________________________USER__________________________________________

class RepositorioUsers():
    def __init__(self, db: Session):
        self.db = db
    #Cria um novo usuário
    def create(self, user: schemas.User):
        try:
            db_user = models.User(
                name=user.name,
                password=user.password,
                email=user.email
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
    
    #Lista todos os usuários
    def list(self):
        try:
            return self.db.query(models.User).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
    #Busca um usuário pelo id
    def get_email_list(self, email: str):
        try:
            return self.db.query(models.User).filter(models.User.email == email).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
            
    #Deleta um usuário pelo id
    def delete(self, id: int):
        try:
            user = self.db.query(models.User).filter(models.User.id == id).first()
            if user:
                self.db.delete(user)
                self.db.commit()
                return {"message": "User deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
    #Atualiza um usuário pelo id
    def update(self, id: int, user: schemas.User):
        try:
            db_user = self.db.query(models.User).filter(models.User.id == id).first()
            if db_user:
                db_user.name = user.name
                db_user.email = user.email
                db_user.password = user.password
                self.db.commit()
                self.db.refresh(db_user)
                return db_user
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
    #Atualiza o token do usuário
    def updatte_user_token(self, email: str):
        try:
            db_user = self.db.query(models.User).filter(models.User.email == email).first()
            if db_user:
                db_user.token = criar_token({'email': email})
                self.db.commit()
                self.db.refresh(db_user)
                return db_user.token
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
    
    #Faz o login do usuário através do email e senha e atualiza o token
    def login(self, data:schemas.LoginUser):
        try:
            user = self.db.query(models.User).filter(models.User.email == data.email).first()
            if user:
                if user.password == data.password:
                    token = self.updatte_user_token(data.email) #token valido por 3 horas
                    return token
                else:
                    raise HTTPException(status_code=400, detail="Incorrect password")
            else:
                raise HTTPException(status_code=404, detail="User not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
#__________________________________________CLIENT__________________________________________

