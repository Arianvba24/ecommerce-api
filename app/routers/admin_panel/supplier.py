from fastapi import APIRouter,HTTPException,status,Depends
from sqlalchemy.orm import Session
from ... import schemas,models,oauth2
from ...database import engine,SessionLocal



router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin/suppliers")
def get_supplier(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para realizar esta operación")

    suppliers = db.query(models.Supplier).all()

    return {"supplier" : suppliers}


@router.get("/admin/suppliers/{id}")
def get_suppliers(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para realizar esta operación")

    supplier = db.query(models.Supplier).filter(models.Supplier.id == id).first()

    if supplier == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No existe ningún proveedor con el id {id}")

    return {"supplier" : supplier}




@router.post("/admin/create_supplier")
def create_supplier(supplier: schemas.SupplierCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para realizar esta operación")

    supplier_query = db.query(models.Supplier).filter(models.Supplier.company_id == supplier.company_id).first()

    if supplier_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Ya existe una empresa con este NIF. Reviselo y vuelva a escribirlo")

    new_supplier = models.Supplier(**supplier.dict())

    db.add(new_supplier)

    db.commit()

    db.refresh(new_supplier)

    return new_supplier


@router.delete("/admin/delete_supplier/{id}")
def delete_supplier(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para realizar esta operación")

    supplier = db.query(models.Supplier).filter(models.Supplier.id == id)

    if supplier.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No se ha encontrado ningún proveedor con el id {id}")

    supplier.delete(synchronize_session=False)

    db.commit()

    return {"data" : f"Se ha borrado el registro {id} exitosamente"}






@router.put("/admin/update_supplier/{id}")
def update_supplier(id: int,updated_supplier: schemas.SupplierUpdate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios necesarios para realizar esta operación")

    supplier = db.query(models.Supplier).filter(models.Supplier.id == id)

    if supplier.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No hemos encontrado ningún proveedor con el id {id}")

    final_value = updated_supplier.dict()

    supplier.update(final_value,synchronize_session=False)

    db.commit()

    return {"data" : f"El registro {id} se ha editado con éxito"}