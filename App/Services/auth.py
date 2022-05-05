from sqlalchemy.orm import Session
from App import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from App.security import hashing, token
from App.models import User,Role,UserRole
from App.Services.db import db
from App.Services.send_mail import send_email_async
from fastapi.encoders import jsonable_encoder

def append_roles(new_user,request):
    main_roles = [UserRole(userId=new_user.Id,roleId=i)  for i in request.Roles]
    db.add_all(main_roles)
    db.commit()


async def create(request: schemas.CreateAccount, db: Session):
    roles= db.query(Role).where(Role.Id in request.Roles)
    if len(roles) != len(request.Roles):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"roles errors check roles")
    try:
        password = hashing.Hash.bcrypt(request.Password)
        del request.Password
        new_user = User(**request.dict(), HashedPassword=password,IsConfirmed=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        append_roles(new_user,request)
        await send_email_async('confirmation email', [new_user.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experiance with us",buttonText="confirm",buttonLink="/"+token.encrypt(new_user.Id)
            ))
        return schemas.Response(success=True, Data=new_user)
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")


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
        data={"sub": user.Username, "role": user.Roles.Name})
    return {**access_token}
def confirm(request: str, db: Session = Depends(db)):
    try:
            object:User=db.query(User).filter(
                User.Id == token.decrypt(request)).first()
            object.IsConfirmed=True
            del object.Id
            obj_in_data = jsonable_encoder(object)
            db.query(User).filter(
                User.Id == token.decrypt(request)).update(obj_in_data, synchronize_session="fetch")
            db.commit()
            return "Confirmed Successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  
async def reset_password_request(request: str, db: Session = Depends(db)):
    try:
        object:User=db.query(User).filter(
        User.Email == request).first()
        await send_email_async('confirmation email', [object.Email], 
            schemas.TemplateBody(details="thanks for creating account. we hope you take good experiance with us",buttonText="confirm",buttonLink="/"+token.encrypt(object.Id)
            ))
        return "Password been reset Successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  
def reset_password(request: schemas.reset_password, db: Session = Depends(db)):
    try:
            object:User=db.query(User).filter(
                User.Id == token.decrypt(request.id)).first()
            object.HashedPassword= hashing.Hash.bcrypt(request.newPassword)
            del object.Id
            obj_in_data = jsonable_encoder(object)
            db.query(User).filter(
                User.Id == token.decrypt(request)).update(obj_in_data, synchronize_session="fetch")
            db.commit()
            return "Password been reset Successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")  