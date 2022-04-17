from typing import List, Optional

from pydantic import BaseModel


class Role(BaseModel):
    Id: int
    Name: str


class User(BaseModel):
    Id: int
    Username: Optional[str]
    Email: Optional[str]
    PhoneNumber: Optional[str]
    ProfileImage: Optional[str]
    IsActive: Optional[bool]
    Role: Optional[str]

    class Config:
        orm_mode = True


class CreateAccount(BaseModel):
    Username: str
    Email: str
    PhoneNumber:  Optional[str]
    ProfileImage: Optional[str]
    Password: str
    RoleId: int

    class Config:
        orm_mode = True


class LoginForm(BaseModel):
    Username: str
    Password: str


class Item(BaseModel):
    Id: int
    Name: str


class Response(BaseModel):
    success: bool
    Data: object


class ShowUser(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
