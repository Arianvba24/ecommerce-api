# from fastapi import FastAPI,status,HTTPException,APIRouter,Depends
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from ..database import engine,SessionLocal
# from ..import database,schemas,utils,models,oauth2

# router = APIRouter(tags=["Authentication"])

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/login")
# def login(user_credentials: schemas.UserLogin,db:Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

#     # print(user_credentials.username)

#     if user == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado el usuario con email {user_credentials.email}")



#     if not utils.verify(user_credentials.password,user.password):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="La contraseña proporcionada no es valida")

#     access_token = oauth2.create_access_token(data={"user_id" : user.id})

#     # return {"detail" : "Contraseña correcta!"}
#     return {"access_token" : access_token,"token_type" : "bearer"}

# -----------------------------------------------------------------------------------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException,status,Depends
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import SessionLocal



router = APIRouter(tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login_user(user_credentials: schemas.UserLogin,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No se ha encontrado a ningún usuarion con este correo")

    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="La contraseña proporcionada es incorrecta")

    # return {"data" : "La contraseña coincide perfectamente"}
    access_token = oauth2.create_access_token(data={"user_id" : user.id})

    return {"access_token" : access_token,"token_type" : "bearer"}

