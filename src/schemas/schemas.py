from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id:Optional[int] = None
    name: str
    email: str
    password: str

    class Config:
        rom_attributes = True
        
class LoginUser(BaseModel):
    email: str
    password: str
    
    class Config:
        rom_attributes = True
        
class Client(BaseModel):
    id:Optional[int] = None
    name: str
    email: str
    password : str 
    phone: Optional[str] = None
    address: Optional[str] = None
    cnpj: Optional[str] = None
    active: Optional[bool] = False

    class Config:
        rom_attributes = True
        
class ActivateClient(BaseModel):
    id: int

    class Config:
        rom_attributes = True
        
        
class Token(BaseModel):
    token: str

    class Config:
        rom_attributes = True