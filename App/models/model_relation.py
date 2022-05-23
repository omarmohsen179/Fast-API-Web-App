
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL
from App.database.database import Base,engine
from sqlalchemy.orm import relationship

class user_role(Base):
    __tablename__ = "user_role"  
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    role_id= Column(ForeignKey('role.Id'), primary_key=True)
    user = relationship("user", back_populates="roles")
    role = relationship("role", back_populates="users") 
class user_shop(Base):
    __tablename__ = "user_shop" 
    
    shop_id = Column(ForeignKey('shop.Id'), primary_key=True)
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    user = relationship("user", back_populates="shops")
    shop = relationship("shop", back_populates="users") 
    role = relationship("shop_role", back_populates="shop")
    role_id = Column(ForeignKey('shop_role.Id'), primary_key=True)
class shop_role(Base):   
    __tablename__ = "shop_role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    shop = relationship("user_shop", back_populates="role")
class shop_category(Base):   
    __tablename__ = "shop_category"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255))
    image_path = Column(String(255))
    shop = relationship("shop", back_populates="category")
class item_category(Base):   
    __tablename__ = "item_category"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    describe = Column(String(255))
    image_path = Column(String(255))
    item = relationship("item", back_populates="category")
class order_item(Base):   
    __tablename__ = "order_item"
    order_id = Column(ForeignKey('order.Id'), primary_key=True)
    order = relationship("order", back_populates="items")
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="orders")
    quantity = Column(Integer, primary_key=True, index=True, nullable=False)
class wishlist(Base):   
    __tablename__ = "wishlist"
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    user = relationship("user", back_populates="wishlist")
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="wishlist")