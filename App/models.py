
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
    Roles = relationship("Role", back_populates="User")
    RoleId = Column(Integer, ForeignKey("Roles.Id"))


class Role(Base):
    __tablename__ = "Roles"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255), nullable=False)
    User = relationship("User", back_populates="Roles")


class Item(Base):
    __tablename__ = "Item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255))
    # items = relationship("Item", back_populates="owner")\
