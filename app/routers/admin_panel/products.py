from fastapi import APIRouter,HTTPException,status,Depends
from ...database import engine,SessionLocal
from sqlalchemy.orm import Session
from ... import schemas,models,utils,oauth2
from typing import List,Optional


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin/products/{id}",response_model=List[schemas.ProductBase])
def buscar_producto(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegions necesarios para realizar esta acción")

    products = db.query(models.Product).filter(models.Product.id == id)

    return products




@router.get("/admin/products")
def buscar_productos(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegions necesarios para realizar esta acción")

    products = db.query(models.Product).all()

    return {"products" : products}


@router.post("/admin/create_product")
def create_product(product: schemas.ProductCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegions necesarios para realizar esta acción")

    product_query = db.query(models.Product).filter(models.Product.product_name == product.product_name).first()

    if product_query:
        raise HTTPException(status_code=status.HTTP_302_FOUND,detail=f"Ya existe un producto con ese nombre en la base de datos. Use otro nombre")

    new_product = models.Product(product_name=product.product_name,supplier_id=product.supplier_id,price=product.price)

    db.add(new_product)

    db.commit()

    db.refresh(new_product)

    return {"data" : "Producto creado con éxito"}


@router.put("/admin/update_product/{id}")
def update_product(id:int,updated_product: schemas.ProductCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegions necesarios para realizar esta acción")

    product_query = db.query(models.Product).filter(models.Product.id == id)

    product = product_query.first()

    final_product = updated_product.dict()

    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado el producto con el {id}")

    product_query.update(final_product,synchronize_session=False)

    db.commit()

    return {"data" : "Producto editado con éxito"}


@router.delete("/admin/delete_product/{id}")
def delete_product(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegions necesarios para realizar esta acción")

    product_query = db.query(models.Product).filter(models.Product.id == id)

    if product_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha podido encontrar el producto con id {id}")

    product_query.delete(synchronize_session=False)

    db.commit()

    return {"data" : "Producto borrado satisfactoriamente"}

    