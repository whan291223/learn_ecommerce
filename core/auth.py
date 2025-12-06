from typing import Optional
from typing import Annotated
from jose import JWTError, jwt #need to install python-jose

from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from decouple import config #need to install python-decouple
from core.db import get_session

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

def get_current_user( #to create a user need to verify 1.token 2.session
    token: Annotated[str, Depends(oauth2_schema)],
    session: Annotated[Session, Depends(get_session)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credential",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

#37.11