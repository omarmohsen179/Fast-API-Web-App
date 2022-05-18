
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL
from App.database import Base,engine
from sqlalchemy.orm import relationship

class user_role(Base):
    __tablename__ = "user_role"  
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    role_id= Column(ForeignKey('role.Id'), primary_key=True)
    user = relationship("user", back_populates="roles")
    role = relationship("role", back_populates="users") 
class user_shop(Base):
    __tablename__ = "user_shop" 
    user_id = Column(ForeignKey('app_user.Id'), primary_key=True)
    shop_id = Column(ForeignKey('shop.Id'), primary_key=True)
    user = relationship("user", back_populates="shops")
    shop = relationship("shop", back_populates="users") 
    role = relationship("shop_role", back_populates="shop")
    role_id = Column(ForeignKey('shop_role.Id'), primary_key=True)
class shop_role(Base):   
    __tablename__ = "shop_role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    shop = relationship("user_shop", back_populates="role")