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
from App.Services.crud import UserCrud
from datetime import datetime, timedelta
from sqlalchemy.orm import  joinedload
from typing import List, Optional,Any
from sqlalchemy import or_

import base64
domain=dotenv_values("pyvenv.cfg")['domain']
def append_roles(new_user,roles,db):
    main_roles = [UserRole(userId=new_user.Id,roleId=i)  for i in roles]
    db.add_all(main_roles)
    db.commit()
def b64e(s):
    return base64.b64encode(s.encode()).decode()
def b64d(s):
    return base64.b64decode(s).decode()
def datafromate(da):
    return datetime.strptime(da, '%d/%m/%y %H:%M:%S')
async def create(request: schemas.CreateAccount, db: Session):
    user_roles = request.Roles

    role_result = db.query(Role).filter(Role.Id.in_(request.Roles)).all()
    print(role_result)
    if len(role_result) != len(user_roles):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"roles errors check roles")
    try:  
        password = hashing.Hash.bcrypt(request.Password)
        del request.Password,request.Roles
        new_user = User(**request.dict(), HashedPassword=password,IsConfirmed=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        append_roles(new_user,user_roles,db)

        access_token =str( token.create_access_token_confirm(
        data=schemas.ConfirmToken(username=new_user.Username)))
        await send_email_async('confirmation email', [new_user.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experience with us",buttonText="confirm",
            buttonLink=domain+"/confirm?token="+
         b64e(access_token)
            ))
             
        return "you have to confirm your mail" 
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)

def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db)):

    user: schemas.User= db.query(User).filter(or_(User.Username == request.UsernameOrEmail,User.Email == request.UsernameOrEmail)).options(
            joinedload(User.roles).options(
                joinedload(UserRole.role)
        )
        ).first()
    if not user.Id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Your username or password is incorrect.")
        
    if not hashing.Hash.verify(user.HashedPassword, request.Password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")
      
    if not user.IsConfirmed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Please confirm the email")  
        
    roles:List[int]=list(map(lambda e:e.role.Id, user.roles))
    
    access_token: dict = token.create_access_token(
            data=schemas.TokenData(username=user.Username,role=roles))
    return {**access_token,"roles":roles}

def confirm(request: str, db: Session):
        tokenparse:schemas.ConfirmToken = token.verify_token_confirm(b64d(request))
        object:User=db.query(User).filter(User.Username == tokenparse.username).first()
        if object.IsConfirmed:
            return "Already Confirmed"
        object.IsConfirmed=True
        user2= schemas.user_confirm(
            **object.__dict__
        )   
        UserCrud.update(db,user2)
        return "your e-mail been confirmed successfully"


async def reset_password_request(request: str, db: Session = Depends(db)):
    try:
        object:User=db.query(User).filter(
        User.Email == request).first()
        tokenx=schemas.ConfirmToken(username=object.Username)
        access_token =str(token.create_access_token_confirm(tokenx,period=datetime.utcnow()))  
       
        await send_email_async('confirmation email', [object.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experiance with us",buttonText="confirm"
            ,buttonLink=domain+"/reset-password?token="+  b64e(access_token)
            ))
        
        return "e-mail been send"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  
def reset_password(request: schemas.reset_password, db: Session = Depends(db)):
    try:
        tokenparse:schemas.ConfirmToken = token.verify_token_confirm(b64d(request.token))
        
        object: User =db.query(User).filter(User.Username == tokenparse.username).first()

        print(datetime.fromtimestamp(object.LastPasswordReset))
        print(tokenparse.expire_date)
        #print(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
        if object.LastPasswordReset and has_expired( tokenparse.expire_date,datetime.fromtimestamp(object.LastPasswordReset)):
            return "Expaired mail"
        object.HashedPassword= hashing.Hash.bcrypt(request.Password)
        object.LastPasswordReset=datetime.timestamp(datetime.utcnow())
        print( object.LastPasswordReset)
        UserCrud.update(db,schemas.user_confirm(
            **object.__dict__
        ))
        return "Password been reset successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)  
def has_expired(date1,date2):
    timex:float=(date1 - date2).total_seconds()
    print(timex)
    return  timex < 1.0