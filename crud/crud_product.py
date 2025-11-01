from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from model.models import Product, Review
from schema import ProductCreate

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    db_product = Product.model_validate(product_data)
    session.add(db_product)
    try:
        await session.commit()
        await session.refresh(db_product) # fetch product
    except IntegrityError:
        await session.rollback()
        raise
    return db_product

async def get_all_product(session: AsyncSession) -> List[Product]:
    statement = select(Product).options(
            selectinload(Product.category), 
            selectinload(Product.reviews)
            )
    result = await session.exec(statement)
    return result.all()

async def get_product_by_id(product_id: int, session: AsyncSession) -> Optional[Product]:
    statement = select(Product).where(Product.id == product_id).options(
        selectinload(Product.category), 
        selectinload(Product.reviews))
    result = await session.exec(statement)
    return result.one_or_none()

async def get_product_reviews(product_id: int,session: AsyncSession) -> List[Review]:
    statement = select(Review).where(Review.product_id == product_id)
    result = await session.exec(statement)
    return result.all()

# TODO add delete product
async def delete_product(product_id: int, session: AsyncSession):
    statement = select(Product).where(Product.id == product_id)
    result = await session.exec(statement)
    product = result.one_or_none()
    if not product:
        raise ValueError
    try:
        await session.delete(product)
        await session.commit()
    except:
        await session.rollback()
        raise
# TODO add update product