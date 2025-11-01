from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from model.models import User, Review
from schema import UserCreate

async def create_user(userdata: UserCreate, session: AsyncSession) -> User:
    db_user = User.model_validate(userdata)
    session.add(db_user)
    try:
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except IntegrityError: #instead of just raise HTTP on this move to raise in api folder
        await session.rollback()
        raise 

async def get_all_users(session: AsyncSession) -> List[User]:
    statement = select(User).options(selectinload(User.reviews))
    result = await session.exec(statement)
    return result.all()

# async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
#     return await session.get(User, user_id)
async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    statement = select(User).where(User.id == user_id).options(selectinload(User.reviews))
    result = await session.exec(statement)
    return result.one_or_none()

async def get_user_reviews(user_id: int, session: AsyncSession) -> List[Review]:
    user_statement = select(User).where(User.id == user_id).options(selectinload(User.reviews))
    user_result = await session.exec(user_statement)
    user = user_result.one_or_none()
    if not user:
        raise ValueError("User not found")
    
    # reivew_statement = select(Review).where(Review.user_id == user_id)
    # review_result = await session.exec(reivew_statement)
    return user.reviews

#TODO remove user and their relavent??