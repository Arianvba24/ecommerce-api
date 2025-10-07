from fastapi import APIRouter,Depends,HTTPException,status
from ...database import engine,SessionLocal
from sqlalchemy.orm import Session
from ... import oauth2,models,schemas


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/admin/roles")
def get_roles(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posees los permisos necesarios para poder")

    roles = db.query(models.Roles).all()

    return {"roles" : roles}


@router.put("/admin/update_role/{id}")
def update_roles(id:int,updated_role: schemas.RoleUpdate ,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posees los permisos necesarios para poder")

    role_query = db.query(models.Roles).filter(models.Roles.id == id)

    role = role_query.first()

    if role == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha podido encontrar el rol con id {id}")

    final_data = updated_role.dict()

    print(final_data)

    role_query.update(final_data,synchronize_session=False)

    db.commit()

    return {"data" : "Rol editado con éxito"}



    
