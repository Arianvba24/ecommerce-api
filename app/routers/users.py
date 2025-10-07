from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ..database import engine,SessionLocal
from .. import schemas,models,oauth2
from typing import List


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.get("/user/data",response_model=schemas.Normal_User)
def get_user_data(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_data = db.query(models.User).filter(models.User.id == current_user.id_value).first()

    return user_data




