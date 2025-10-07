from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ... import models,schemas,oauth2
from ...database import engine,SessionLocal
from typing import Optional,List


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @router.get("/admin/sales",response_model=List[schemas.SalesBase])
# @router.get("/admin/sales",response_model=List[schemas.SalesBase])
@router.get("/admin/sales")
def get_sales(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para acceder a esta sección")

    sales = db.query(models.Sale).all()


    return sales



@router.get("/admin/sales/{id}",response_model=List[schemas.SalesBase])
def get_sale(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posees los permisos necesarios para llevar a cabo esta acción")

    sale = db.query(models.Sale).filter(models.Sale.id == id).first()

    if sale == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado ningún registro con el id {id}")

    return sale


@router.put("/admin/update_sale/{id}")
def update_sale(id: int,updated_sale: schemas.SalesUpdate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posees los permisos necesarios para llevar a cabo esta acción")

    sale_query = db.query(models.Sale).filter(models.Sale.id == id)

    sale = sale_query.first()

    if sale == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha podido encontrar el registro con id {id}")

    new_sale = updated_sale.dict()

    sale_query.update(new_sale,synchronize_session=False)

    db.commit()

    return {"data" : f"Registro {id} actualizado con éxito"}


@router.delete("/admin/delete_sale/{id}")
def delete_sale(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posees los permisos necesarios para llevar a cabo esta acción")

    sale = db.query(models.Sale).filter(models.Sale.id == id)

    if sale.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha podido encontrar el registro con id {id}")

    
    sale.delete(synchronize_session=False)

    db.commit()

    return {"data" : f"Se ha borrado el registro con id {id}"}
    


    

