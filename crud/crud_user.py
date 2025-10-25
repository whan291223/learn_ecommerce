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
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists."
        )

async def get_all_users(session: AsyncSession) -> List[User]:
    statement = select(User).options(selectinload(User.reviews))
    result = await session.exec(statement)
    return result.all()

async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[User]:
    return await session.get(User, user_id)

async def get_user_reviews(user_id: int, session: AsyncSession) -> List[Review]:
    statement = select(Review).where(Review.user_id == user_id)
    result = await session.exec(statement)
    return result.all()