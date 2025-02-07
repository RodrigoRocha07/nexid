from fastapi import FastAPI, Depends, Request
from fastapi import status
from src.infra.repositorios.repositorio import RepositorioUsers
from fastapi.responses import RedirectResponse
from src.infra.config.database import criar_db, get_db
from sqlalchemy.orm import Session
from src.schemas import schemas 




app = FastAPI(
    title="API NEXID",
    description="Authentication API with KYC (Know Your Customer) Technology.",
    version="1.0.0"
)

#___________________________________________________HOME

@app.get('/',tags=["Documentation"])
async def home():
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)


#___________________________________________________USERS

@app.get("/users/list", tags=["users"])
async def users(request: Request,db:Session = Depends(get_db)):
    users = RepositorioUsers(db).list()
    return users

@app.post("/users/create", tags=["users"])
async def create_user(data: schemas.User,db:Session = Depends(get_db)):
    RepositorioUsers(db).create(data)    
    return {"message": "User created successfully"}


@app.delete("/users/delete/{id}", tags=["users"])
async def delete_user(id:str,db:Session = Depends(get_db)):
    RepositorioUsers(db).delete(id)
    return {"message": "User deleted successfully"}

@app.put("/users/update/{id}", tags=["users"])
async def update_user(id:str,data: schemas.User,db:Session = Depends(get_db)):
    RepositorioUsers(db).update(id,data)
    return {"message": "User updated"}

#___________________________________________________auth


