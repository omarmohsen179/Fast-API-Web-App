
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from App.Services.db import db
from App import schemas,models
from App.Services import crud, auth
from sqlalchemy.orm import  joinedload
from App.security import Oauth
from fastapi import status, HTTPException
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)



@router.get('/'
)
async def get_user(db: Session = Depends(db)):
    db_books = db.query(models.User).options(
        joinedload(models.User.roles).options(
            joinedload(models.UserRole.role)
        )
    ).all() 
    return db_books



@router.post('/create-account')
def createAccount(request: schemas.CreateAccount, db: Session = Depends(db)):
    return auth.create(request, db)


@router.post('/login')
def Login(request: schemas.LoginForm, db: Session = Depends(db)):
    return auth.login(request, db)
@router.post('/reset-password-request/{email}')
def ResetRequest(email: str, db: Session = Depends(db)):
    return auth.reset_password_request(email, db)
@router.post('/reset-password')
def Reset(email: schemas.reset_password, db: Session = Depends(db)):
    return auth.reset_password(email, db)
@router.post('/confirm/{id}')
def ResetRequest(id: int,  db: Session = Depends(db)):
    return auth.confirm(id, db)
@router.get('/admin')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(lambda e:Oauth.get_current_admin(e))):
    return "admin"


@router.get('/user')
def Login(db: Session = Depends(db), current_admin: schemas.User = Depends(Oauth.get_current_user)):
    return "user"


@router.delete('/{id}')
def createAccount(id: int, db: Session = Depends(db)):
    return crud.UserCrud.delete(db, id)
@router.post('/check-email/{email}')
def check_email(email: str, db: Session = Depends(db)):
    user_email=crud.UserCrud.get(db).filter(models.User.email == str)
    if  len(user_email) >0: 
        return 200
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="email is taken")
@router.post('/check-email/{username}')
def check_email(email: str, db: Session = Depends(db)):
    user_email=crud.UserCrud.get(db).filter(models.User.email == str)
    if  len(user_email) >0: 
        return 200
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="email is taken")
@router.delete('/all/')
def createAccount(db: Session = Depends(db)):
    return crud.UserCrud.delete_all(db)
