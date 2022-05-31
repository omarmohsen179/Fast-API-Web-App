
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
from App.database.database import Base,engine,SessionLocal
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
    orders = relationship("order", back_populates="user")
    roles = relationship("user_role", back_populates="user")

class shop(Base):   
    __tablename__ = "shop"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_shop", back_populates="shop")
    items = relationship("item", back_populates="shop")
class item(Base):   
    __tablename__ = "item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    item_name = Column(String(255), nullable=False)
    item_describe = Column(String(255), nullable=False)
    order_item = relationship("order_item", back_populates="item")
    category_id = Column(Integer,ForeignKey('item_category.Id'))
    category = relationship("item_category", back_populates="items")
    shop_id = Column(Integer,ForeignKey('shop.Id'))
    shop = relationship("shop", back_populates="items")
    item_images = relationship("item_image", back_populates="item")
    wishlist = relationship("wishlist", back_populates="item")

class order(Base):   
    __tablename__ = "order"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    total_cost=  Column(Integer, default=0, nullable=False)
    note = Column(String(255), nullable=False)
    date = Column( DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    user_id = Column(Integer,ForeignKey('app_user.Id'))
    user = relationship("user", back_populates="orders")
    order_item = relationship("order_item", back_populates="order")
    


class role(Base):   
    __tablename__ = "role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_role", back_populates="role")
class offer_item(Base):   
    __tablename__ = "offer_item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    date =Column(DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    quantity =Column(Integer, nullable=True)
    offer_id = Column(ForeignKey('offer.Id'))
    offer = relationship("offer", back_populates="offers_item")
    item_id = Column(ForeignKey('item.Id'))
    item = relationship("item", back_populates="item_offers")
    
class wishlist(Base):   
    __tablename__ = "wishlist"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(ForeignKey('app_user.Id'))
    user = relationship("user", back_populates="wishlist")
    item_id = Column(ForeignKey('item.Id'))
    item = relationship("item", back_populates="wishlist")






with Session(bind=engine) as session:
    users = [user(Id=1,username="admin",email="admin123@gmail.com",hashed_password=hashing.Hash.bcrypt("admin"))]
    roles = [role(Id=1,name="Blogs"),
             role(Id=2,name="Sale"),
             role(Id=3,name="Web Admin"),
             role(Id=4,name="User Admin"),
             ]
    user_roles=[user_role(user_id=users[0].Id, role_id=roles[0].Id)
                ,user_role(user_id=users[0].Id, role_id=roles[1].Id),
                user_role(user_id=users[0].Id, role_id=roles[2].Id)
                ,user_role(user_id=users[0].Id, role_id=roles[3].Id)]
    session.add_all(users)
    session.add_all(roles)
    session.add_all(user_roles)