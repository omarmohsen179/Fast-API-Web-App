
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL,DateTime
from App.database import Base,engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from datetime import datetime
from  App.security import hashing
from  App.models.model_relation import *
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
class role(Base):   
    __tablename__ = "role"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_role", back_populates="role")
class shop(Base):   
    __tablename__ = "shop"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    users = relationship("user_shop", back_populates="shop")



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