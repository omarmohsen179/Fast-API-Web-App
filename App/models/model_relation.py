
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL,DateTime
from App.database.database import Base,engine
from sqlalchemy.orm import relationship
from datetime import datetime
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
class keyword(Base):   
    __tablename__ = "keyword"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    keyword = Column(String(255), nullable=False)
    items= relationship("keyword_item", back_populates="keyword")
class keyword_item(Base):   
    __tablename__ = "keyword_item"
    keyword_id = Column(ForeignKey('keyword.Id'), primary_key=True)
    keyword = relationship("keyword", back_populates="items")
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="keywords")
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
    quantity = Column(Integer, nullable=False)
class wishlist(Base):   
    __tablename__ = "wishlist"
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    user = relationship("user", back_populates="wishlist")
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="wishlist")
class offer_item(Base):   
    __tablename__ = "offer_item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    date =Column(DateTime, nullable=True,default=datetime.utcnow().strftime("%Y-%m-%d" "%H:%M:%S"))
    quantity =Column(Integer, nullable=True)
    offer_id = Column(ForeignKey('offer.Id'), primary_key=True)
    offer = relationship("offer", back_populates="offers_item")
    item_id = Column(ForeignKey('item.Id'), primary_key=True)
    item = relationship("item", back_populates="item_offers")