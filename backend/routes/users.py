from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from auth import create_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter_by(username=user.username).first()
    if not db_user or db_user.password != user.password:
        return {"msg": "Invalid credentials"}
    token = create_token({"user": user.username})
    return {"access_token": token}
