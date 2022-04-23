from typing import List, Optional

from pydantic import validator, BaseModel


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


class TemplateBody(BaseModel):
    buttonText: Optional[str]
    details: Optional[str]
    helpLink: Optional[bool]
    unsubscribeMail: Optional[str]

    class Config:
        orm_mode = True


class CreateAccount(BaseModel):
    Username: str
    Email: str
    PhoneNumber:  Optional[str]
    ProfileImage: Optional[str]
    Password: str
    RoleId: int

    @validator('Username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator("PhoneNumber")
    def phone_length(cls, v):
        if len(str(v)) != 10:
            raise ValueError("Phone number must be of ten digits")
        return v

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


class ImageResponse(BaseModel):
    isOk: bool
    result: object


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
