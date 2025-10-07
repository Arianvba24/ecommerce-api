from fastapi import FastAPI,status,HTTPException,APIRouter,Depends
from .routers.admin_panel import products,users,roles,supplier,sales
from .routers import auth
# from . import 
from . import models
from .database import engine,SessionLocal
from .routers import users as router_user
from .routers import sales as router_sales


models.Base.metadata.create_all(bind=engine)



app = FastAPI()

# Admin and login routers---------------------
app.include_router(users.router)
app.include_router(products.router)
app.include_router(roles.router)
app.include_router(supplier.router)
app.include_router(sales.router)
app.include_router(auth.router)

#User routers---------------------------------
app.include_router(router_user.router)
app.include_router(router_sales.router)
