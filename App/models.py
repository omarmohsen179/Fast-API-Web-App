
from typing_extensions import Required
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from App.database import Base
from App.services.crud import crud


class User(Base):
    __tablename__ = "Appuser"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Username = Column(String(255), unique=True, index=True, nullable=False)
    Email = Column(String(255), unique=True, index=True, nullable=False)
    HashedPassword = Column(String(255), nullable=False)
    PhoneNumber = Column(String, nullable=True)
    ProfileImage = Column(String, nullable=True)
    IsActive = Column(Boolean, default=True)
    #items = relationship("Item", back_populates="owner")


class UserCrud(crud):
    def __init__(self):
        self.model = User


class Item(Base):
    __tablename__ = "Item"
    Id = Column(Integer, primary_key=True, index=True, nullable=False)
    Name = Column(String(255))
    #items = relationship("Item", back_populates="owner")


class ItemCrud(crud):
    def __init__(self):
        self.model = Item
