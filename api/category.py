from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_category
from schema import CategoryCreate, CategoryPublic, ProductPublic

router = APIRouter(prefix="categories", tags=['categories'])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=CategoryPublic)
async def create_new_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session)
) -> CategoryPublic:
    new_category = await crud_category.create_category(category_data=category_data, session=session)
    return new_category

@router.get("/", response_model=List[CategoryPublic])
async def get_all_category(
    session: AsyncSession = Depends(get_session)
) -> List[CategoryPublic]:
    categories = await crud_category.get_all_category(session)
    return categories

@router.get("/{category_id}", response_model=CategoryPublic)
async def get_category_by_id(
    category_id: int,
    session: AsyncSession = Depends(get_session)
) -> CategoryPublic:
    category = await crud_category.get_category_by_id(category_id=category_id, session=session)
    return category

@router.get("/{category_name}/products}", response_model=List[ProductPublic])
async def get_category_products(
    category_name: str,
    session: AsyncSession = Depends(get_session)
) -> List[ProductPublic]:
    products = await crud_category.get_category_products(category_name=category_name, session=session)
    return products