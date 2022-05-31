
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from App.security import token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    mytoken = token.verify_token(data, credentials_exception)
    return mytoken


def get_current_admin(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    mytoken = token.verify_token(data, credentials_exception)
    if(mytoken.role != "Admin"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="unauthrized")
    return mytoken
def sale_auth(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    mytoken = token.verify_token(data, credentials_exception)
    if(mytoken.role != "Sale"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="unauthrized")
    return mytoken
