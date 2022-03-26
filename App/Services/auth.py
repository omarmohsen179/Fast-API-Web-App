from sqlalchemy.orm import Session
import App.schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, HTTPException
from App.security.hashing import Hash
from App.security import token
import App.models


def create(request: App.schemas.CreateAccount, db: Session):
    password = Hash.bcrypt(request.Password)
    print(password)

    new_user = App.models.User(Username=request.Username, Email=request.Email,
                               HashedPassword=password, PhoneNumber=request.PhoneNumber)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return App.schemas.Response(success=True, Data=new_user)
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=App.schemas.Response(success=False, Data=err))


def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(App.database.get_db)):
    user = db.query(App.models.User).filter(
        App.models.User.Username == request.Username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    if not Hash.verify(user.HashedPassword, request.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")

    access_token = token.create_access_token(data={"sub": user.Username})
    return {"access_token": access_token, "token_type": "bearer"}
