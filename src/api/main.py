from fastapi import FastAPI, Depends, Request
from fastapi import status
from src.infra.repositorios.repositorio import RepositorioUsers, RepositorioClients
from fastapi.responses import RedirectResponse
from src.infra.config.database import criar_db, get_db
from sqlalchemy.orm import Session
from src.schemas import schemas 
from typing import Dict
from src.providers import token_provider


app = FastAPI(
    title="API NEXID",
    description="Authentication API with KYC (Know Your Customer) Technology.",
    version="1.0.0"
)

#___________________________________________________HOME

@app.get('/',tags=["Documentation"])
async def home():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


@app.post("/create-database", tags=["Database"])
async def create_database():
    criar_db()
    return {"message": "Database created successfully"}

#___________________________________________________USERS

@app.get("/users/list", tags=["Users"])
async def users(request: Request,db:Session = Depends(get_db)):
    users = RepositorioUsers(db).list()
    return users

@app.post("/users/create", tags=["Users"])
async def create_user(data: schemas.User,db:Session = Depends(get_db)):
    RepositorioUsers(db).create(data)    
    return {"message": "User created successfully"}


@app.delete("/users/delete/{id}", tags=["Users"])
async def delete_user(id:str,db:Session = Depends(get_db)):
    RepositorioUsers(db).delete(id)
    return {"message": "User deleted successfully"}

@app.put("/users/update/{id}", tags=["Users"])
async def update_user(id:str,data: schemas.User,db:Session = Depends(get_db)):
    RepositorioUsers(db).update(id,data)
    return {"message": "User updated"}

#___________________________________________________auth

@app.post("/auth/login", tags=["Auth"])
async def login(data: schemas.LoginUser ,db:Session = Depends(get_db)):
    token = RepositorioUsers(db).login(data)
    return {"token": token}

@app.post("/auth/validateToken", tags=["Auth"])
async def validate_token(data: Dict,db:Session = Depends(get_db)):
    token = data['token']
    return token_provider.verificar_token(token)

#___________________________________________________client

@app.post("/client/create", tags=["Client"])
async def create_client(data: schemas.Client,db:Session = Depends(get_db)):
    RepositorioClients(db).create(data)   
    return {"message": "Client created successfully"}


@app.post("/client/activate", tags=["Client"])
async def activate_client(data: schemas.ActivateClient ,db:Session = Depends(get_db)):
    RepositorioClients(db).activate(data.id)
    return {"message": "Client activated successfully"}