from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_product
from schema import ProductCreate, ProductPublic

router = APIRouter() # router will initiate path for api automaticly
#  ex. .post('product/xyz') -> .post('xyz')

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=ProductPublic)
async def create_new_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_session)
):