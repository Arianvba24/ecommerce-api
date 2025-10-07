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

@router.get("/user/sales",response_model=List[schemas.SalesBase])
def get_user_data(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_sales = db.query(models.Sale).filter(models.Sale.user_id == current_user.id_value).all()

    if user_sales == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado ningún registro con su id")

    return user_sales


@router.post("/user/create_sale")
def create_sale(sale: schemas.SalesCreate,db:Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    sale.user_id = current_user.id_value
    
    new_sale = models.Sale(**sale.dict())

    db.add(new_sale)

    db.commit()

    db.refresh(new_sale)

    return {"data" : "Venta creada con exito"}
