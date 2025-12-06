from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db import get_session
from crud import crud_user
from schema import UserPublic, UserCreate, ReviewPublic, UserPublicWithoutReview

from typing import Annotated
from core.auth import create_accessL_token
from fastapi.security import OAuth2PasswordRequestForm
from core.security import verify_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublicWithoutReview)
async def create_user(
    userdata: UserCreate, 
    session: AsyncSession = Depends(get_session)
) -> UserPublicWithoutReview:
    try:
        user = await crud_user.create_user(userdata=userdata, session=session) 
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )


@router.get("/", response_model=List[UserPublic])
async def get_all_users(
    session: AsyncSession = Depends(get_session)
) -> List[UserPublic]:
    users = await crud_user.get_all_users(session=session)
    return users

@router.get("/user_id/{user_id}", response_model=UserPublic)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> UserPublic:
    user = await crud_user.get_user_by_id(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User id:{user_id} not found")
    return user

@router.get("/username/{username}", response_model=UserPublic)
async def get_user_by_username(
    username: str,
    session: AsyncSession = Depends(get_session)
) -> UserPublic:
    user = await crud_user.get_user_by_username(username=username, session=session)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User name:{username} not found")
    return user

@router.get("/{user_id}/reviews", response_model=List[ReviewPublic])
async def get_user_reviews(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[ReviewPublic]:
    try:
        reviews = await crud_user.get_user_reviews(user_id=user_id, session=session)
        return reviews
    except ValueError:
        raise HTTPException(status_code=404, detail=f"User id:{user_id} not found")


async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm,
        session: AsyncSession = Depends(get_session)
):
    try:
        user = await crud_user.create_user(userdata=form_data.username, session=session) 
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )
    #TODO