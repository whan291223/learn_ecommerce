from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from model.models import Category, Product
from schema import CategoryCreate

async def create_category(category_data: CategoryCreate, session: AsyncSession) -> Category:
    db_category = Category.model_validate(category_data)
    session.add(db_category)
    try:
        await session.commit()
        await session.refresh(db_category) # fetch product
        return db_category
    except IntegrityError:
        await session.rollback()
        raise

async def get_all_category(session: AsyncSession) -> List[Category]:
    statement = select(Category).options(selectinload(Category.products))
    result = await session.exec(statement)
    return result.all()

async def get_category_by_id(category_id: int, session: AsyncSession) -> Optional[Category]:
    statement = select(Category).where(Category.id == category_id)
    result = await session.exec(statement)
    return result.one_or_none()

async def get_category_by_name(category_name: str, session: AsyncSession) -> Optional[Category]:
    statement = select(Category).where(Category.name == category_name)
    result = await session.exec(statement)
    return result.one_or_none()

async def get_category_products(category_name: str,
                                session: AsyncSession
                                ) -> List[Product]:
    statement = select(Category).where(Category.name == category_name)
    result = await session.exec(statement)
    category =  result.one_or_none()
    if not category:
        return []
    return category.products