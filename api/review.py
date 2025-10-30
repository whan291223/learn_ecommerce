from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from core.db import get_session
from crud import crud_review
from schema import ReviewCreate, ReviewPublic

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewPublic)
async def create_review(
    review_data: ReviewCreate, 
    session: AsyncSession = Depends(get_session)
    ) -> ReviewPublic:
    try:
        review = await crud_review.create_review(review_data=review_data, session=session)
        return review
    except IntegrityError as integrity_error:
        if hasattr(integrity_error.orig, "diag") and getattr(integrity_error.orig.diag, "message_detail", None):
            detail = integrity_error.orig.diag.message_detail
        else:
            detail = str(integrity_error.orig)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
     

@router.get("/{review_id}", response_model=ReviewPublic)
async def get_review_by_id(
    review_id: int,
    session: AsyncSession = Depends(get_session)
) -> ReviewPublic:
    try:
        review = await crud_review.get_review_by_id(review_id=review_id, session=session) 
        return review
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Review id: {review_id} not found")

@router.get("/", response_model=List[ReviewPublic])
async def get_all_reviews(
    session: AsyncSession = Depends(get_session)
) -> List[ReviewPublic]:
    reviews = await crud_review.get_all_reviews(session=session)
    return reviews