from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_review
from schema import ReviewCreate, ReviewPublic

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewPublic)
async def create_review(
    review_data: ReviewCreate, 
    session: AsyncSession = Depends(get_session)
    ) -> ReviewCreate:
    review = await crud_review.create_review(review_data=review_data, session=session)
    return review

@router.get("/{review_id}", response_model=ReviewPublic)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session)
) -> ReviewPublic:
    review = await crud_review.get_review_by_id(review_id=review_id, session=session) 
    return review