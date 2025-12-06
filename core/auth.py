from typing import Optional
from typing import Annotated
from jose import JWTError, jwt #need to install python-jose

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decouple import config #need to install python-decouple

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token") #coming from fastapi

def create_accessL_token(data: dict,expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


