
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from App.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "Appuser"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Username = Column(String(255), unique=True, index=True, nullable=False)
    Email = Column(String(255), unique=True, index=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    PhoneNumber = Column(String, nullable=True)
    ProfileImage = Column(String, nullable=True)
    IsActive = Column(Boolean, default=True)
    RoleId = Column(Integer, ForeignKey("Roles.Id"))
    Roles = relationship("Role", back_populates="Users")


class Role(Base):
    __tablename__ = "Roles"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    Users = relationship("User", back_populates="Roles")
    # items = relationship("Item", back_populates="owner")\
