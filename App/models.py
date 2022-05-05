
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from App.database import Base,engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.ext.associationproxy import association_proxy

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
    PhoneNumber = Column(String, nullable=True)
    ProfileImage = Column(String, nullable=True)
    IsActive = Column(Boolean, default=False, nullable=False)
    IsConfirmed = Column(Boolean, default=False, nullable=False)
    roles = relationship("UserRole", back_populates="user")


class Role(Base):   
    __tablename__ = "Roles"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    users = relationship("UserRole", back_populates="role")

with Session(bind=engine) as session:
    users = [User(Id=1,Username="User2212ss22",Email="Ema22ssil1222",HashedPassword="dsdsdsddsdsd")]
    roles = [Role(Id=2,Name="Blogs"),
             Role(Id=3,Name="Items")]
    user_roles=[UserRole(userId=users[0].Id, roleId=roles[0].Id)
                ,UserRole(userId=users[0].Id, roleId=roles[1].Id)]
    #session.add_all(users)
    #session.add_all(roles)
    #session.add_all(user_roles)
    #session.commit()