from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db import get_session
from crud import crud_product_variant
from schema.product_variant_schema import ProductVariantCreate,ProductVariantUpdate,ProductVariantPublic

router = APIRouter(prefix="/product-variants", tags=["product-variant"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductVariantPublic)
async def create_product_variant(
    variant_data: ProductVariantCreate,
    session: AsyncSession = Depends(get_session)
) -> ProductVariantPublic:
    try:
        variant = await crud_product_variant.create_variant(
            variant_data=variant_data,
            session=session
        )
        return variant
    except IntegrityError as integrity_error:
        detail = str(integrity_error.orig)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


@router.get("/", response_model=List[ProductVariantPublic])
async def get_all_variants(
    session: AsyncSession = Depends(get_session)
) -> List[ProductVariantPublic]:
    variants = await crud_product_variant.get_all_variants(session=session)
    return variants

@router.get("/{variant_id}", response_model=ProductVariantPublic)
async def get_variant_by_id(
    variant_id: int,
    session: AsyncSession = Depends(get_session)
) -> ProductVariantPublic:
    variant = await crud_product_variant.get_variant_by_id(
        variant_id=variant_id,
        session=session
    )

    if not variant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variant with id {variant_id} not found!"
        )

    return variant

@router.get("/product/{product_id}", response_model=List[ProductVariantPublic])
async def get_variants_by_product(
    product_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[ProductVariantPublic]:
    variants = await crud_product_variant.get_variants_by_product(
        product_id=product_id,
        session=session
    )
    return variants

@router.put("/", response_model=ProductVariantPublic)
async def update_variant(
    variant_data: ProductVariantUpdate,
    session: AsyncSession = Depends(get_session)
) -> ProductVariantPublic:
    try:
        variant = await crud_product_variant.update_variant(
            variant_data=variant_data,
            session=session
        )
        return variant
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variant id {variant_data.id} not found!"
        )
    except IntegrityError as integrity_error:
        detail = str(integrity_error.orig)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )

@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(
    variant_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await crud_product_variant.delete_variant(
            variant_id=variant_id,
            session=session
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variant id {variant_id} not found!"
        )
