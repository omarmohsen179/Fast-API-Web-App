
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.database.db import db
from App.models import schemas, models
from App.Services import crud, auth
from sqlalchemy.orm import joinedload
from App.security import Oauth
from fastapi import status, HTTPException
router = APIRouter(
    prefix="/api/auth",
    tags=['auth']
)


@router.get('/',
            # response_model=List[schemas.user]
            )
async def get_user(db: Session = Depends(db)):
    db_books: List[schemas.user] = db.query(models.user).options(
        joinedload(models.user.roles).options(
            joinedload(models.user_role.role)
        )
    ).all()
    return db_books


@router.post('/create-account')
async def createAccount(request: schemas.create_account, db: Session = Depends(db)):
    request.roles = [1, 2]
    create = await auth.create(request, db)
    return create


@router.post('/login')
def Login(request: schemas.login_form, db: Session = Depends(db)):
    return auth.login(request, db)


@router.post('/reset-password-request/{email}')
async def ResetRequest(email: str, db: Session = Depends(db)):
    return await auth.reset_password_request(email, db)


@router.post('/reset-password')
def Reset(email: schemas.reset_password, db: Session = Depends(db)):
    return auth.reset_password(email, db)


@router.post('/confirm')
def ResetRequest(token: schemas.token,  db: Session = Depends(db)):
    try:
        resualt = auth.confirm(token.value, db)
        return resualt
    except BaseException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=err.args)


@router.get('/admin')
def Login(db: Session = Depends(db), current_admin: schemas.user = Depends(lambda e: Oauth.get_current_admin(e))):
    return "admin"


@router.put('')
def update(request: schemas.update_user, db: Session = Depends(db)):
    try:
        resualt = dict((k, v)
                       for k, v in request.dict().items() if v is not None)
        main = dict((k, v) for k, v in (db.query(models.user).filter(
            models.user.Id == request.Id)).__dict__.items() if v is not None and k not in resualt.keys())
        user2 = schemas.User(
            **main, **resualt
        )
        del user2.roles
        return crud.user_crud.update(db, user2)
    except BaseException as err:
        return err.args


@router.get('/user')
def Login(db: Session = Depends(db), current_admin: schemas.user = Depends(Oauth.get_current_user)):
    return "user"


@router.delete('/{id}')
def deleteuser(id: int, db: Session = Depends(db)):
    return crud.user_crud.delete(db, id)


@router.post('/check-email/{email}')
def check_email(email: str, db: Session = Depends(db)):
    user_email = crud.user_crud.get(db).filter(
        models.User.email == email).all()
    if len(user_email) > 0:
        return 200
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email is taken")


@router.post('/check-username/{username}')
def check_email(username: str, db: Session = Depends(db)):

    user_username = crud.user_crud.get(db).filter(
        models.User.username == username).all()
    if len(user_username) > 0:
        return 200
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="email is taken")


@router.delete('/all/')
def createAccount(db: Session = Depends(db)):
    crud.user_role_crud.delete_all(db)
    return crud.user_crud.delete_all(db)
