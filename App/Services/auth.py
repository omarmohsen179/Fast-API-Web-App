from sqlalchemy.orm import Session
from App.models import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from App.security import hashing, token
from App.models.models import user, role, user_role
from App.database.db import db
from App.Services.send_mail import send_email_async
from fastapi.encoders import jsonable_encoder
from dotenv import dotenv_values
from App.Services.crud import user_crud
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from typing import List, Optional, Any
from sqlalchemy import or_

import base64
domain = dotenv_values("pyvenv.cfg")['domain']


def append_roles(new_user, roles, db):
    main_roles = [user_role(user_id=new_user.Id, role_id=i) for i in roles]
    db.add_all(main_roles)
    db.commit()


def b64e(s):
    return base64.b64encode(s.encode()).decode()


def b64d(s):
    return base64.b64decode(s).decode()


def datafromate(da):
    return datetime.strptime(da, '%d/%m/%y %H:%M:%S')


async def create(request: schemas.create_account, db: Session):
    user_roles = request.roles
    role_result = db.query(role).filter(role.Id.in_(request.roles)).all()
    if len(role_result) != len(user_roles):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"roles errors check roles")
    try:

        password = hashing.Hash.bcrypt(request.password)
        print(password)
        del request.password, request.roles
        new_user = user(**request.dict(),
                        hashed_password=password, is_confirmed=False)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        append_roles(new_user, user_roles, db)

        access_token = str(token.create_access_token_confirm(
            data=schemas.confirm_token(username=new_user.username)))
        await send_email_async('confirmation email', [new_user.email],
                               schemas.template_body(details="thanks for creating account. we hope you take good experience with us", buttonText="confirm",
                                                     buttonLink=domain+"/confirm?token=" +
                                                     b64e(access_token)
                                                     ))

        return "you have to confirm your mail"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)


def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db)):

    user: schemas.User = db.query(user).filter(or_(user.username == request.UsernameOrEmail, user.email == request.UsernameOrEmail)).options(
        joinedload(user.roles).options(
            joinedload(user_role.role)
        )
    ).first()
    if not user.Id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Your username or password is incorrect.")

    if not hashing.Hash.verify(user.HashedPassword, request.Password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")

    if not user.is_confirmed:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Please confirm the email")

    roles: List[int] = list(map(lambda e: e.role.Id, user.roles))

    access_token: dict = token.create_access_token(
        data=schemas.TokenData(username=user.username, role=roles))
    return {**access_token, "roles": roles}


def confirm(request: str, db: Session):
    tokenparse: schemas.confirm_token = token.verify_token_confirm(
        b64d(request))
    object: user = db.query(user).filter(
        user.username == tokenparse.username).first()
    if object.is_confirmed:
        return "Already Confirmed"
    object.is_confirmed = True
    user2 = schemas.user_confirm(
        **object.__dict__
    )
    user_crud.update(db, user2)
    return "your e-mail been confirmed successfully"


async def reset_password_request(request: str, db: Session = Depends(db)):
    try:
        object: user = db.query(User).filter(
            user.email == request).first()
        tokenx = schemas.confirm_token(username=object.username)
        access_token = str(token.create_access_token_confirm(
            tokenx, period=datetime.utcnow()))

        await send_email_async('confirmation email', [object.email],
                               schemas.template_body(details="thanks for creating account. we hope you take good experiance with us", buttonText="confirm", buttonLink=domain+"/reset-password?token=" + b64e(access_token)
                                                     ))

        return "e-mail been send"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something went wrong")


def reset_password(request: schemas.reset_password, db: Session = Depends(db)):
    try:
        tokenparse: schemas.confirm_token = token.verify_token_confirm(
            b64d(request.token))

        object: user = db.query(user).filter(
            user.username == tokenparse.username).first()

        print(datetime.fromtimestamp(object.LastPasswordReset))
        print(tokenparse.expire_date)
        # print(datetime.fromtimestamp(datetime.timestamp(datetime.now())))
        if object.LastPasswordReset and has_expired(tokenparse.expire_date, datetime.fromtimestamp(object.LastPasswordReset)):
            return "Expaired mail"
        object.HashedPassword = hashing.Hash.bcrypt(request.Password)
        object.LastPasswordReset = datetime.timestamp(datetime.utcnow())
        print(object.LastPasswordReset)
        UserCrud.update(db, schemas.user_confirm(
            **object.__dict__
        ))
        return "Password been reset successfully"
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)


def has_expired(date1, date2):
    timex: float = (date1 - date2).total_seconds()
    print(timex)
    return timex < 1.0
