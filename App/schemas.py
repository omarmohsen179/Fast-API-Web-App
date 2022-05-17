from typing import List, Optional,Any
from datetime import date, datetime, timedelta
from pydantic import validator, BaseModel,EmailStr




class Role(BaseModel):
    Id: int
    Name: str
    class Config:
        orm_mode = True
class Token(BaseModel):
    value: str
    class Config:
        orm_mode = True

class UserRole(BaseModel):
    role:Optional[Role] 
    class Config:
        orm_mode = True
class User(BaseModel):
    Id : int
    Username:  Optional[str]
    Email :  Optional[str]
    HashedPassword :  Optional[str]
    PhoneNumber:  Optional[str]
    FullName :  Optional[str]
    ProfileImage :  Optional[str]
    IsActive :  Optional[bool]
    IsConfirmed :  Optional[bool]
    LastPasswordReset :  Optional[Any]
    roles :  List[UserRole]
    def dict(self, **kwargs):
        data = super(User, self).dict(**kwargs)
        print(data['roles'])
        for b in data['roles']:
            b['Id']=b['role']['Id']
            b['Name'] = b['role']['Name']
            del b['role']

        return data
    class Config:
        orm_mode = True
class user_confirm(BaseModel):
    Id : int
    Username:  Optional[str]
    Email :  Optional[str]
    HashedPassword :  Optional[str]
    PhoneNumber:  Optional[str]
    FullName :  Optional[str]
    ProfileImage :  Optional[str]
    IsActive :  Optional[bool]
    IsConfirmed :  Optional[bool]
    LastPasswordReset :  Optional[Any]
    class Config:
        orm_mode = True

class UpdateUser(BaseModel):
    Id : Optional[int]=None
    Username:  Optional[str]=None
    Email :  Optional[str]=None
    PhoneNumber:  Optional[str]=None
    FullName :  Optional[str]=None
    ProfileImage :  Optional[str]=None
    class Config:
        orm_mode = True


class TemplateBody(BaseModel):
    buttonText: Optional[str]
    details: Optional[str]
    helpLink: Optional[bool]
    unsubscribeMail: Optional[str]
    buttonLink:Optional[str]
    class Config:
        orm_mode = True
class reset_password(BaseModel):
    Password: Optional[str]
    token:Optional[str]
    class Config:
        orm_mode = True

class CreateAccount(BaseModel):
    Username: str
    Email: EmailStr
    PhoneNumber:  Optional[str]
    ProfileImage: Optional[str]
    Password: str
    Roles: Optional[List[int]]
    @validator('Username')
    def username_alphanumeric(cls, v):
        #assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator("PhoneNumber")
    def phone_length(cls, v):
        if len(str(v)) != 10:
            raise ValueError("Phone number must be of ten digits")
        return v

    class Config:
        orm_mode = True


class LoginForm(BaseModel):
    UsernameOrEmail: str
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


class ConfirmToken(BaseModel):
    username: Optional[str] = None
    expire_date: Optional[str]= None


class ImageResponse(BaseModel):
    isOk: bool
    result: object


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[List[int]] = None
    expire_date: Optional[str] = None
    