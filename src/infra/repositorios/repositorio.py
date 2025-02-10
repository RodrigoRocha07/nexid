from src.infra.config.database import criar_db, get_db
from src.infra.models import models
from sqlalchemy.orm import Session
from src.schemas import schemas
from src.providers.token_provider import *
from typing import Dict
from fastapi import HTTPException
from src.utils.disparo_email import *
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
    
#_________________________________________AUTH__________________________________________


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

class RepositorioClients():
    def __init__(self, db: Session):
        self.db = db
    #Cria um novo cliente
    def create(self, client: schemas.Client):
        try:
            db_client = models.Client(
                name=client.name,
                cnpj=client.cnpj,
                email=client.email,
                phone=client.phone,
                address=client.address
            )
            
            self.db.add(db_client)
            self.db.commit()
            self.db.refresh(db_client)
            solicitacao_registro(db_client.id,client.name)
            ativacao_em_analise(client.name,client.email)
            return db_client
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
    
    #Ativa um cliente pelo id
    def activate(self, id: int):
        try:
            db_client = self.db.query(models.Client).filter(models.Client.id == id).first()
            if db_client:
                db_client.active = True
                self.db.commit()
                self.db.refresh(db_client)
                confirmacao_registro(db_client.name,db_client.email)
                return db_client
            else:
                raise HTTPException(status_code=404, detail="Client not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
    
    #Lista todos os clientes
    def list(self):
        try:
            return self.db.query(models.Client).all()
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
    #Busca um cliente pelo id
    def get(self, id: int):
        try:
            return self.db.query(models.Client).filter(models.Client.id == id).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
            
    #Deleta um cliente pelo id
    def delete(self, id: int):
        try:
            client = self.db.query(models.Client).filter(models.Client.id == id).first()
            if client:
                self.db.delete(client)
                self.db.commit()
                return {"message": "Client deleted successfully"}
            else:
                raise HTTPException(status_code=404, detail="Client not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
        
    #Atualiza um cliente pelo id
    def update(self, id: int, client: schemas.Client):
        try:
            db_client = self.db.query(models.Client).filter(models.Client.id == id).first()
            if db_client:
                db_client.name = client.name
                db_client.cpf = client.cpf
                db_client.email = client.email
                db_client.phone = client.phone
                db_client.address = client.address
                self.db.commit()
                self.db.refresh(db_client)
                return db_client
            else:
                raise HTTPException(status_code=404, detail="Client not found")
        except Exception as e:
            raise HTTPException(status_code=400, detail={"message": str(e), "severity": "error"})
    