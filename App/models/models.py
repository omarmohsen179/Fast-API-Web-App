
from pydoc import describe
from unicodedata import category
from sqlalchemy import Boolean, Column, Float, Integer, String, ForeignKey,REAL,DateTime
from App.database.database import Base,engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from datetime import datetime
from  App.security import hashing
from  App.models.model_relation import *

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL,DateTime
from App.database.database import Base,engine
from sqlalchemy.orm import relationship
from datetime import datetime

class user(Base):
    __tablename__ = "app_user"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    phone_number = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    profile_image = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=False, nullable=True)
    is_confirmed = Column(Boolean, default=False, nullable=False)
    last_password_reset = Column(REAL, nullable=True)
    date_of_birth = Column( DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    shops = relationship("user_shop", back_populates="user")
class user_shop(Base):
    __tablename__ = "user_shop" 
    shop_id = Column(ForeignKey('shop.Id'), primary_key=True)
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    user = relationship("user", back_populates="shops")
    shop = relationship("shop", back_populates="users") 
class shop(Base):   
    __tablename__ = "shop"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_shop", back_populates="shop")
    items = relationship("item", back_populates="shop")
    role = relationship("shop_role", back_populates="shop")
    role_id = Column(ForeignKey('shop_role.Id'), primary_key=True)
class shop_role(Base):   
    __tablename__ = "shop_role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    shop = relationship("user_shop", back_populates="role")
class role(Base):   
    __tablename__ = "role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_role", back_populates="role")
class user_role(Base):
    __tablename__ = "user_role"  
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    role_id= Column(ForeignKey('role.Id'), primary_key=True)
    user = relationship("user", back_populates="roles")
    role = relationship("role", back_populates="users") 
class item(Base):   
    __tablename__ = "item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255), nullable=False)
    category_id = Column(ForeignKey('item_category.Id'), primary_key=True)
    category = relationship("item_category", back_populates="items")
    shop_id = Column(ForeignKey('shop.Id'), primary_key=True)
    shop = relationship("shop", back_populates="items")
    
class item_category(Base):   
    __tablename__ = "item_category"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255))
    image_path = Column(String(255))
    items = relationship("item", back_populates="category")
