from sqlalchemy.orm import Session
import App.schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, status, HTTPException
from App.Security import hashing
from App.Security import token
import App.models


def create(request: App.schemas.CreateAccount, db: Session):

    try:
        password = hashing.Hash.bcrypt(request.Password)
        del request.Password
        new_user = App.models.User(**request.dict(), HashedPassword=password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return App.schemas.Response(success=True, Data=new_user)
    except BaseException as err:
        cc = App.schemas.Response(success=False, Data=err)
        print(cc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"something happend")


def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(App.database.get_db)):
    user = db.query(App.models.User).filter(
        App.models.User.Username == request.Username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Credentials")
    if not hashing.Hash.verify(user.HashedPassword, request.Password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Incorrect password")
    access_token: dict = token.create_access_token(
        data={"sub": user.Username, "role": user.Roles.Name})
    return {**access_token}
