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
    expire = (datetime.utcnow() + timedelta(days=int(dotenv_values("pyvenv.cfg")['durationInDays']))).strftime('%d/%m/%y %H:%M:%S')
    data.expire_date=expire
    encoded_jwt = jwt.encode(data.dict(), dotenv_values(
        "pyvenv.cfg")['secretkey'], algorithm=ALGORITHM)
    return {"token": encoded_jwt, "expire_date": expire}


def verify_token(token: str, credentials_exception):
    try:
        
        payload = jwt.decode(token, dotenv_values(
            "pyvenv.cfg")['secretkey'], algorithms=[ALGORITHM])
        
        username: str = payload.get("username")
        role: str = payload.get("role")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username, role=role)
        return token_data
    except JWTError:
        raise credentials_exception
def create_access_token_confirm(data: schemas.ConfirmToken,period=(datetime.utcnow() + timedelta(hours=int(dotenv_values("pyvenv.cfg")['durationInDays'])))):
  
    data.expire_date=period.strftime('%d/%m/%y %H:%M:%S')
    print(period) 
    encoded_jwt:str = jwt.encode(data.dict(), dotenv_values(
        "pyvenv.cfg")['secretkey'], algorithm=ALGORITHM)
    return encoded_jwt

def verify_token_confirm(token: str)-> schemas.ConfirmToken:
    try:
        payload = jwt.decode(token, dotenv_values("pyvenv.cfg")['secretkey'], algorithms=[ALGORITHM])
        payload=schemas.ConfirmToken(**payload)
        datee :datetime=datetime.strptime(payload.expire_date, '%d/%m/%y %H:%M:%S')
        payload.expire_date= datee
        #if has_expired(datee):
            #raise Error("expaired token")
        return payload
    except JWTError as err:
        raise  

def has_expired(date):
    timex:float=(date - datetime.now() ).total_seconds()
    return  timex < 1.0
