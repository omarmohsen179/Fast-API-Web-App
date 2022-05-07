from sqlalchemy.orm import Session
from App import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from App.security import hashing, token
from App.models import User,Role,UserRole
from App.Services.db import db
from App.Services.send_mail import send_email_async
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
import base64
domain=dotenv_values("pyvenv.cfg")['domain']
def append_roles(new_user,roles,db):
    main_roles = [UserRole(userId=new_user.Id,roleId=i)  for i in roles]
    db.add_all(main_roles)
    db.commit()


async def create(request: schemas.CreateAccount, db: Session):
    user_roles = request.Roles
    roles= db.query(Role)
    [roles.filter(Role.Id== number) for number in user_roles]
    if len(roles.all()) != len(user_roles):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"roles errors check roles")

    try:  
        password = hashing.Hash.bcrypt(request.Password)
        del request.Password
        del request.Roles
        new_user = User(**request.dict(), HashedPassword=password,IsConfirmed=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        append_roles(new_user,user_roles,db)
        access_token: dict = token.create_access_token(
        data={"us": new_user.Username})
  
        await send_email_async('confirmation email', [new_user.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experience with us",buttonText="confirm",
            buttonLink=domain+"/confirm?token="+
            access_token['token']
            ))
             
        return "you have to confirm your mail" 
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)


def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db)):
    user = db.query(User).filter(
        User.Username == request.Username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")
    if not hashing.Hash.verify(user.HashedPassword, request.Password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")
    access_token: dict = token.create_access_token(
        data={"sub": user.Username, "role": user.roles[0].roleId})
    return {**access_token}
def confirm(request: str, db: Session = Depends(db)):
    try:
        idx = token.decrypt(base64.b64decode(request))
        object:User=db.query(User).filter(User.Id == idx).first()
        object.IsConfirmed = True
        del object.Id
        obj_in_data = jsonable_encoder(object)
        db.query(User).filter(
                User.Id == idx).update(obj_in_data, synchronize_session="fetch")
        db.commit()
        return "Confirmed Successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  
async def reset_password_request(request: str, db: Session = Depends(db)):
    try:
        tokenx=base64.b64encode(token.encrypt(object.Id))
        object:User=db.query(User).filter(
        User.Email == request).first()
        await send_email_async('confirmation email', [object.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experiance with us",buttonText="confirm"
            ,buttonLink=domain+"/reset-password?t="+tokenx
            ))
        return "Email been send"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  
def reset_password(request: schemas.reset_password, db: Session = Depends(db)):
    try:
        idx= token.decrypt(base64.b64decode(request.id))
        object:User=db.query(User).filter(User.Id == idx).first()
        object.HashedPassword= hashing.Hash.bcrypt(request.newPassword)
        del object.Id
        obj_in_data = jsonable_encoder(object)
        db.query(User).filter(User.Id == idx).update(obj_in_data, synchronize_session="fetch")
        db.commit()
        return "Password been reset Successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  