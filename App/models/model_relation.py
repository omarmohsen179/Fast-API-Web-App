
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

class order_item(Base):   
    __tablename__ = "order_item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    item_id = Column(Integer,ForeignKey('item.Id'))
    item = relationship("item", back_populates="order_item")
    order_id = Column(Integer,ForeignKey('order.Id'))
    order = relationship("order", back_populates="order_item")
class item_category(Base):   
    __tablename__ = "item_category"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255))
    image_path = Column(String(255))
    items = relationship("item", back_populates="category")
class user_role(Base):
    __tablename__ = "user_role"  
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer,ForeignKey('app_user.Id'))
    role_id= Column(Integer,ForeignKey('role.Id'))
    user = relationship("user", back_populates="roles")
    role = relationship("role", back_populates="users") 
class user_shop(Base):
    __tablename__ = "user_shop" 
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    shop_id = Column(Integer,ForeignKey('shop.Id'))
    user_id = Column(Integer,ForeignKey('app_user.Id'))
    user = relationship("user", back_populates="shops")
    shop = relationship("shop", back_populates="users") 
class item_image(Base):   
    __tablename__ = "item_image"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    image_path = Column(String(255), nullable=False)
    item_id = Column(ForeignKey('item.Id'))
    item = relationship("item", back_populates="item_images")
class offer_item(Base):   
    __tablename__ = "offer_item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    date =Column(DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    quantity =Column(Integer, nullable=True)
    offer_id = Column(ForeignKey('offer.Id'))
    offer = relationship("offer", back_populates="offers_item")
    item_id = Column(ForeignKey('item.Id'))
    item = relationship("item", back_populates="item_offers")
#extend_existing=True