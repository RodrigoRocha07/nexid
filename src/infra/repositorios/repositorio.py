from src.infra.config.database import criar_db, get_db
from src.infra.models import models
from sqlalchemy.orm import Session
from src.schemas import schemas

class RepositorioUsers():
    def __init__(self, db: Session):
        self.db = db
        
    def create(self, user: schemas.User):
        db_user = models.User(
            name=user.name,
            password=user.password,
            email=user.email
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def list(self):
        return self.db.query(models.User).all()
    
    def get_email_list(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()

    def delete(self, id):
        user = self.db.query(models.User).filter(models.User.id == id).first()
        self.db.delete(user)
        self.db.commit()
        return 'User deleted successfully'
    
    def update(self, id, user: schemas.User):
        db_user = self.db.query(models.User).filter(models.User.id == id).first()
        db_user.name = user.name
        db_user.email = user.email
        db_user.password = user.password
        self.db.commit()
        self.db.refresh(db_user)
        return db_user