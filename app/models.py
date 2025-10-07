from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    username = Column(String(length=17),nullable=False,unique=True)
    email = Column(String(length=30),nullable=False,unique=True)
    password = Column(String(length=150),nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,nullable=False)
    product_name = Column(String(length=80),unique=True,nullable=False)
    price = Column(Integer,nullable=False)
    supplier_id = Column(Integer,ForeignKey("supplier.id"),nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))

class Supplier(Base):
    __tablename__ = "supplier"
    id = Column(Integer,primary_key=True,nullable=False)
    company_name = Column(String(length=70),unique=True,nullable=False)
    company_id = Column(String,unique=True,nullable=False)
    contact_name = Column(String,nullable=False)
    contact_number = Column(String,nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer,primary_key=True,nullable=False)
    units = Column(Integer,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("NOW()"))
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    product  = relationship("Product")
    

class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    role = Column(String,nullable=False)

    
