from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import User, Review
from schema import UserCreate

async def create_user(userdata: UserCreate, session: AsyncSession) -> User:
    db_user = User.model_validate(userdata)
    session.add(db_user)
    await session.commit()
    await session.refresh()
    return db_user

async def get_user_reviews(user_id: int, session: AsyncSession) -> List[Review]:
    statement = select(Review).where(Review.user_id == user_id)
    result = await session.exec(statement)
    return result.all()

async def get_all_user(session: AsyncSession) -> List[User]:
    statement = select(User)
    result = await session.exec(statement)
    return result.all()

async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    return await session.get(User, user_id)