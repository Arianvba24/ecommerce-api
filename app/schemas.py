from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id_value : Optional[str] = None


class ProductBase(BaseModel):
    id: int
    product_name: str
    supplier_id: int
    create_at: datetime
    price: int

    class Config:
        from_attributes =  True

class SalesBase(BaseModel):
    id: int
    product: ProductBase
    user_id : int
    units: int
    create_at: datetime

    class Config:
        from_attributes =  True


class SalesUpdate(BaseModel):
    product_id: int
    units: int

class SalesCreate(BaseModel):
    units : int
    user_id : Optional[int] = None
    product_id : int

        

class ProductCreate(BaseModel):
    product_name: str
    supplier_id: int
    price: int

class ProductUpdate(ProductCreate):
    pass


class RoleUpdate(BaseModel):
    role: str

class SupplierBase(BaseModel):
    company_name:str
    company_id: str
    contact_name:str
    contact_number:str


class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(SupplierBase):
    pass

class Normal_User(BaseModel):
    username : str
    email: EmailStr
    create_at : datetime


    class Config:
        from_attributes =  True







  