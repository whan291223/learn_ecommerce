from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Review
from schema import ReviewCreate

async def create_review(review_data: ReviewCreate, session: AsyncSession) -> Review:
    db_review = Review.model_validate(review_data)
    session.add(db_review)
    await session.commit(db_review)
    await session.refresh()
    return db_review

async def get_review_by_id(review_id: int, session: AsyncSession) -> Review:
    return await session.get(Review, review_id) #can only use session.get where the query parameter is primary key
    
# async def get_product_reviews(product_id: int,session: AsyncSession) -> List[Review]:
#     statement = select(Review).where(Review.product_id == product_id)
#     result = await session.exec(statement)
#     return result.all()

# async def get_user_reviews(user_id: int, session: AsyncSession) -> List[Review]:
#     statement = select(Review).where(Review.user_id == user_id)
#     result = await session.exec(statement)
#     return result.all()