from sqlalchemy.orm import Session
import App.schemas
from fastapi import HTTPException, status
from App.hashing import Hash
import App.models


def create(request: App.schemas.User, db: Session):
    password = Hash.bcrypt(request.Password)
    print(password)

    new_user = App.models.User(Username=request.Username, Email=request.Email,
                               HashedPassword=password, PhoneNumber=request.PhoneNumber)

    print(new_user)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return App.schemas.Response(success=True, Data=new_user)
    except BaseException as err:
        print("Variable x is not defined")
        return App.schemas.Response(success=False, Data=err)
