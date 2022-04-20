from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from App import schemas
from dotenv import dotenv_values
from typing import Optional
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=int(dotenv_values(
            "pyvenv.cfg")['duration-in-days']))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, dotenv_values(
        "pyvenv.cfg")['secret-key'], algorithm=ALGORITHM)
    return {"token": encoded_jwt, "expire_date": expire}


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, dotenv_values(
            "pyvenv.cfg")['secret-key'], algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")

        print(username)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)
        return token_data
    except JWTError:
        raise credentials_exception
