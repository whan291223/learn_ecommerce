from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from model.models import Category
from schema import CategoryBase, CategoryCreate

async def create_category(category_data: CategoryCreate, session: AsyncSession) -> Category:
    db_category = Category.model_validate(category_data)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category) # fetch product
    return db_category

async def get_all_category(session: AsyncSession) -> List[Category]:
    statement = select(Category)
    result = await session.exec(statement)
    return result.all()

async def get_category_by_id(category_id: int, session: AsyncSession) -> Optional[Category]:
    statement = select(Category).where(Category.id == category_id)
    result = await session.exec(statement)
    return result.one_or_none()