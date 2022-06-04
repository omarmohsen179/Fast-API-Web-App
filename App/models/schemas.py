from typing import List, Optional, Any
from datetime import date, datetime, timedelta
from pydantic import validator, BaseModel, EmailStr


class role(BaseModel):
    Id: int
    name: str

    class Config:
        orm_mode = True


class categories(BaseModel):
    Id: Optional[int]
    name: Optional[str]
    name_en: Optional[str]
    describe: Optional[str]
    describe_en: Optional[str]
    image_path: Optional[str]

    class Config:
        orm_mode = True


class token(BaseModel):
    value: str

    class Config:
        orm_mode = True


class user_role(BaseModel):
    role: Optional[role]

    class Config:
        orm_mode = True


class user(BaseModel):
    Id: int
    username:  Optional[str]
    email:  Optional[str]
    hashed_password:  Optional[str]
    phone_number:  Optional[str]
    full_name:  Optional[str]
    profile_image:  Optional[str]
    is_active:  Optional[bool]
    is_confirmed:  Optional[bool]
    last_password_reset:  Optional[Any]
    roles:  List[user_role]

    def dict(self, **kwargs):
        print(data['roles'])
        data = super(user, self).dict(**kwargs)
        for b in data['roles']:
            b['Id'] = b['role']['Id']
            b['name'] = b['role']['name']
            del b['role']

        return data

    class Config:
        orm_mode = True


class user_confirm(BaseModel):
    Id: int
    username:  Optional[str]
    email:  Optional[str]
    hashed_password:  Optional[str]
    phone_number:  Optional[str]
    full_name:  Optional[str]
    profile_image:  Optional[str]
    is_active:  Optional[bool]
    is_confirmed:  Optional[bool]
    last_password_reset:  Optional[Any]

    class Config:
        orm_mode = True


class update_user(BaseModel):
    Id: Optional[int] = None
    username:  Optional[str] = None
    email:  Optional[str] = None
    hashed_password:  Optional[str] = None
    phone_number:  Optional[str] = None
    full_name:  Optional[str] = None
    profile_image:  Optional[str] = None

    class Config:
        orm_mode = True


class template_body(BaseModel):
    buttonText: Optional[str]
    details: Optional[str]
    helpLink: Optional[bool]
    unsubscribeMail: Optional[str]
    buttonLink: Optional[str]

    class Config:
        orm_mode = True


class reset_password(BaseModel):
    Password: Optional[str]
    token: Optional[str]

    class Config:
        orm_mode = True


class Banner(BaseModel):
    title: str
    text: str


class create_account(BaseModel):
    username: str
    email: EmailStr
    phone_number:  Optional[str]
    profile_image: Optional[str]
    password: str
    roles: Optional[List[int]]

    @validator('username')
    def username_alphanumeric(cls, v):
        #assert v.isalnum(), 'must be alphanumeric'
        return v

    @validator("phone_number")
    def phone_length(cls, v):
        if len(str(v)) != 10:
            raise ValueError("Phone number must be of ten digits")
        return v

    class Config:
        orm_mode = True


class login_form(BaseModel):
    UsernameOrEmail: str
    Password: str


class item(BaseModel):
    Id: int
    Name: str


class response(BaseModel):
    success: bool
    Data: object


class show_user(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: show_user

    class Config():
        orm_mode = True


class login(BaseModel):
    username: str
    password: str


class confirm_token(BaseModel):
    username: Optional[str] = None
    expire_date: Optional[str] = None


class image_response(BaseModel):
    isOk: bool
    result: object


class token_data(BaseModel):
    username: Optional[str] = None
    role: Optional[List[int]] = None
    expire_date: Optional[str] = None
