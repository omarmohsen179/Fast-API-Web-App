from typing import List, Optional
from pydantic import BaseModel


class User(BaseModel):
    Username: str
    Email: str
    Password: str
    PhoneNumber:  Optional[str]
    ProfileImage: Optional[str]


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
    email: Optional[str] = None
