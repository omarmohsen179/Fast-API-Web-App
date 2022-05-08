from datetime import datetime, timedelta
from msilib.schema import Error
from jose import jwt
from jose.exceptions import JWTError
from App import schemas
from dotenv import dotenv_values
from typing import Optional
import   json 
ALGORITHM = "HS256"

def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
def create_access_token(data: schemas.TokenData):
    expire = datetime.utcnow() + timedelta(days=int(dotenv_values("pyvenv.cfg")['durationInDays']))
    data.expire_date=expire
    encoded_jwt = jwt.encode(data, dotenv_values(
        "pyvenv.cfg")['secretkey'], algorithm=ALGORITHM)
    return {"token": encoded_jwt, "expire_date": expire}


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, dotenv_values(
            "pyvenv.cfg")['secretkey'], algorithms=[ALGORITHM])
        username: str = payload.get("username")
        role: str = payload.get("role")

        print(username)
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)
        return token_data
    except JWTError:
        raise credentials_exception
def create_access_token_confirm(data: schemas.ConfirmToken):
    datex :str=json.dumps(datetime.utcnow() + timedelta(days=int(dotenv_values("pyvenv.cfg")['durationInDays'])), indent=4, sort_keys=True, default=str).replace('"','  ')
    data.expire_date=datex

    encoded_jwt:str = jwt.encode(data.dict(), dotenv_values(
        "pyvenv.cfg")['secretkey'], algorithm=ALGORITHM)
    return encoded_jwt
from dateutil.parser import parse
def verify_token_confirm(token: str)-> schemas.ConfirmToken:
    try:
       
        payload = jwt.decode(token, dotenv_values("pyvenv.cfg")['secretkey'], algorithms=[ALGORITHM])
        
        payload=schemas.ConfirmToken(**payload)
        print("------------------")
        print(payload.expire_date)
        s = "2016-03-26T09:25:55.000"
        f = "%Y-%m-%dT%H:%M:%S.%f"
        "2022-05-22 02:59:05.415203"
        print(datetime.strptime(s, f))
        if has_expired(datetime.strptime(payload.expire_date, f)):
            raise Error("expaired token")
        print(datetime(payload.expire_date)) 
        return payload
    except JWTError as err:
        raise  

def has_expired(date):
    return date < datetime.now()
