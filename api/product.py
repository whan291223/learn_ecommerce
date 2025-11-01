from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db import get_session
from crud import crud_product
from schema import ProductCreate, ProductPublic, ProductCategoryID, ReviewPublic

router = APIRouter(prefix="/products", tags=["product"]) # router will initiate path for api automaticly
#  ex. .post('product/xyz') -> .post('xyz')

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductCategoryID)
async def create_new_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_session)
) -> ProductCategoryID: #fix add default factoty field for reviews, and use differrent schema for show only category_id
    try:
        new_product = await crud_product.create_product(product_data=product_data, session=session)
        return new_product
    except IntegrityError as integrity_error:
        if hasattr(integrity_error.orig, "diag") and getattr(integrity_error.orig.diag, "message_detail", None):
            detail = integrity_error.orig.diag.message_detail
        else:
            detail = str(integrity_error.orig)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

@router.get("/", response_model=List[ProductPublic])
async def get_all_product(
    session: AsyncSession = Depends(get_session)
) -> List[ProductPublic]:
    products = await crud_product.get_all_product(session=session)
    return products

@router.get("/{product_id}", response_model=ProductPublic)
async def get_product_detail(
    product_id: int,
    session: AsyncSession = Depends(get_session)
) -> ProductPublic:
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found!")
    return product

@router.get("/{product_id}/reviews", response_model=List[ReviewPublic])
async def get_product_reviews(
    product_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[ReviewPublic]:
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found!")

    return product.reviews

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await crud_product.delete_product(product_id=product_id, session=session)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Product id: {product_id} not found")