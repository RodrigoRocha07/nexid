from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    id:Optional[int] = None
    name: str
    email: str
    password: str

    class Config:
        rom_attributes = True
