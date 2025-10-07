from fastapi import FastAPI,status,HTTPException,APIRouter,Depends
from sqlalchemy.orm import Session
# from .database import engine,SessionLocal
from ...database import engine,SessionLocal
# from .. import models
from ...import models,utils,oauth2
from ...import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/admin/users")
def get_users(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posees los privilegios necesarios para interactuar con esta API")

    users = db.query(models.User).all()
    return users
    

@router.get("/admin/users/{id}")
def get_one_user(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail=f"No posee los privilegios necesarios para acceder a esta información")

    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado ningún usuario con ese id")



    return user


# @router.post("/testing")
# def testing_posts(user: schemas.UserCreate,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user)):
#     print("Hola--------------------------------------------")
#     new_user = models.User(**user.dict())

#     db.add(new_user)

#     db.commit()
    

#     return new_user



@router.post("/admin/create_user",status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
# def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No posee los privilegios necesarios para acceder a esta información")

    

    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    user_username = db.query(models.User).filter(models.User.username == user.username).first()
    
    user_email = db.query(models.User).filter(models.User.email == user.email).first()

    if user_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"El usuario {user.username} ya existe. Utilize otro nombre para crear un usuario")

    if user_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"El usuario con email {user.email} ya existe. Utilize otro email para crear un usuario")

    # Creating new user-----------------------------------
    new_user = models.User(username=user.username,email=user.email,password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Creating a role user--------------------------------
    user_id = db.query(models.User).filter(models.User.email == user.email).first()
    role_user = models.Roles(id=user_id.id,role="user")
    db.add(role_user)
    db.commit()
    db.refresh(role_user)

    return {"data" : "Usuario creado con éxito"}


@router.delete("/admin/delete/{id}")
def delete_user(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios suficientes para acceder a este espacio")


    user = db.query(models.User).filter(models.User.id == id)

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado el usuario con id {id}. Vuélvalo a intentar")

    user.delete(synchronize_session=False)

    db.commit()
    return {"data" : f"Usuario {id} eliminado!"}
    



@router.put("/admin/modify_user/{id}")
def modify_user(id:int,user: schemas.UserUpdate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    user_role = db.query(models.Roles).filter(models.Roles.id == current_user.id_value).first()

    if user_role.role != "admin":
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="No posee los privilegios suficientes para acceder a este espacio")

    user_query = db.query(models.User).filter(models.User.id == id)

    hashed_password = utils.hash(user.password)

    user.password = hashed_password

    user_value = user.dict()

    user = user_query.first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha podido encontrar el usuario con id {id}")

    # ------------------------------------------
    
    print(user_value)


    
    user_query.update(user_value,synchronize_session=False)

    db.commit()

    return {"data" : "Updated succesfully"}
    


