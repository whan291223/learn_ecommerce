from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_user
from schema import UserPublic, UserCreate, ReviewPublic

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserPublic)
async def create_user(
    userdata: UserCreate, 
    session: AsyncSession = Depends(get_session)
) -> UserPublic:
    user = await crud_user.create_user(userdata=userdata, session=session) 
    return user

@router.get("/", response_model=List[UserPublic])
async def get_all_users(
    session: AsyncSession = Depends(get_session)
) -> List[UserPublic]:
    users = await crud_user.get_all_users(session=session)
    return users

@router.get("/{user_id}", response_model=UserPublic)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> UserPublic:
    user = await crud_user.get_user_by_id(user_id=user_id, session=session)
    return user

@router.get("/{user_id}/reviews", response_model=List[ReviewPublic])
async def get_user_reviews(
    user_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[ReviewPublic]:
    reviews = await crud_user.get_user_reviews(user_id=user_id, session=session)
    return reviews

