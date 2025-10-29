from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from model.models import Review
from schema import ReviewCreate
#TODO api still error when create review
# product reviews in product api still error
async def create_review(review_data: ReviewCreate, session: AsyncSession) -> Review:
    db_review = Review.model_validate(review_data)
    session.add(db_review)
    try:
        await session.commit()
        await session.refresh(db_review)
        return db_review
    except IntegrityError:
        await session.rollback()
        raise

async def get_review_by_id(review_id: int, session: AsyncSession) -> Review:
    #TODO missing greenlet
    return await session.get(Review, review_id) #can only use session.get where the query parameter is primary key
    
# async def get_product_reviews(product_id: int,session: AsyncSession) -> List[Review]:
#     statement = select(Review).where(Review.product_id == product_id)
#     result = await session.exec(statement)
#     return result.all()

# async def get_user_reviews(user_id: int, session: AsyncSession) -> List[Review]:
#     statement = select(Review).where(Review.user_id == user_id)
#     result = await session.exec(statement)
#     return result.all()