
from pydoc import describe
from unicodedata import category
from sqlalchemy import Boolean, Column, Float, Integer, String, ForeignKey,REAL,DateTime
from App.database.database import Base,engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from datetime import datetime
from  App.security import hashing
from  App.models.model_relation import *
class shop(Base):   
    __tablename__ = "shop"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)

    name = Column(String(255), nullable=False)
    items = relationship("item",uselist=True, back_populates="shop_x")
    users = relationship("user_shop", back_populates="shop")
    category_id = Column(ForeignKey('shop_category.Id'), primary_key=True)
    category = relationship("shop_category", back_populates="shop")
class item(Base):   
    __tablename__ = "item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255), nullable=False)
    shop_id = Column(ForeignKey('shop.Id'), primary_key=True)
    shop_x:shop = relationship("shop", back_populates="items")
    category_id = Column(ForeignKey('item_category.Id'), primary_key=True)
    category = relationship("item_category", back_populates="item")
    offers = relationship("offer_item", back_populates="item")
    item_images = relationship("item_image", back_populates="item")
    orders = relationship("order_item", back_populates="item")
    wishlist = relationship("wishlist", back_populates="item")
    
    keywords = relationship("keyword_item", back_populates="item")

    

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
    roles = relationship("user_role", back_populates="user")
    shops = relationship("user_shop", back_populates="user")
    orders = relationship("order", back_populates="user")
    wishlist = relationship("wishlist",   
        cascade="all,delete-orphan",
        uselist=True,back_populates="user")

class role(Base):   
    __tablename__ = "role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_role", back_populates="role")

class order(Base):   
    __tablename__ = "order"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    note = Column(String(255), nullable=False)
    date = Column( DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    user = relationship("user", back_populates="orders")
    items = relationship("order_item", back_populates="order")
    total_cost=  Column(Float, default=0, nullable=False)




class item_image(Base):   
    __tablename__ = "item_image"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    image_path = Column(String(255), nullable=False)
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="item_images")



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
    #session.commit()