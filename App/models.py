
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey,REAL
from App.database import Base,engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from  App.security import hashing

class UserRole(Base):
    __tablename__ = "UserRole"  

    userId = Column(ForeignKey('Appuser.Id'), primary_key=True)
    roleId = Column(ForeignKey('Roles.Id'), primary_key=True)
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users") 
class User(Base):
    __tablename__ = "Appuser"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Username = Column(String(255), unique=True, index=True, nullable=False)
    Email = Column(String(255), unique=True, index=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    PhoneNumber = Column(String(255), nullable=True)
    FullName = Column(String(255), nullable=True)
    ProfileImage = Column(String(255), nullable=True)
    IsActive = Column(Boolean, default=False, nullable=True)
    IsConfirmed = Column(Boolean, default=False, nullable=False)
    LastPasswordReset = Column(REAL, nullable=True)
    roles = relationship("UserRole", back_populates="user")


class Role(Base):   
    __tablename__ = "Roles"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    users = relationship("UserRole", back_populates="role")

with Session(bind=engine) as session:
    users = [User(Id=1,Username="admin",Email="admin123@gmail.com",HashedPassword=hashing.Hash.bcrypt("admin"))]
    roles = [Role(Id=1,Name="Blogs"),
             Role(Id=2,Name="Sale"),
             Role(Id=3,Name="Web Admin"),
             Role(Id=4,Name="User Admin"),
             ]
    user_roles=[UserRole(userId=users[0].Id, roleId=roles[0].Id)
                ,UserRole(userId=users[0].Id, roleId=roles[1].Id),
                UserRole(userId=users[0].Id, roleId=roles[2].Id)
                ,UserRole(userId=users[0].Id, roleId=roles[3].Id)]
    session.add_all(users)
    session.add_all(roles)
    session.add_all(user_roles)
    #session.commit()