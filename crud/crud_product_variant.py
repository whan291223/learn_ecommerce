from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import ProductVariant, Product
from schema.product_variant_schema import ProductVariantCreate, ProductVariantUpdate

async def create_variant(
    variant_data: ProductVariantCreate,
    session: AsyncSession
) -> ProductVariant:
    
    # Make sure product exists
    result = await session.exec(select(Product).where(Product.id == variant_data.product_id))
    product = result.first()
    if not product:
        raise ValueError("Product not found")
    
    db_product_variant = ProductVariant.model_validate(variant_data)
    session.add(db_product_variant)
    await session.commit()
    await session.refresh(db_product_variant)
    return db_product_variant


async def get_all_variants(session: AsyncSession) -> list[ProductVariant]:
    result = await session.exec(
        select(ProductVariant).where(ProductVariant.is_active == True)
    )
    return result.all()

async def get_all_in_active_variants(session: AsyncSession) -> list[ProductVariant]:
    result = await session.exec(
        select(ProductVariant).where(ProductVariant.is_active == False)
    )
    return result.all()

async def get_variant_by_id(
    variant_id: int,
    session: AsyncSession
) -> ProductVariant | None:

    result = await session.exec(
        select(ProductVariant).where(ProductVariant.id == variant_id)
    )
    return result.first()

async def get_variants_by_product(
    product_id: int,
    session: AsyncSession
) -> list[ProductVariant]:
    result = await session.exec(
        select(ProductVariant)
        .where(ProductVariant.product_id == product_id)
        .where(ProductVariant.is_active == True)
    )
    return result.all()

async def update_variant(
    variant_data: ProductVariantUpdate,
    session: AsyncSession
) -> ProductVariant:
    variant = await get_variant_by_id(variant_data.id, session)
    if not variant:
        raise ValueError("Variant not found")

    update_data = variant_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(variant, key, value)

    session.add(variant)
    await session.commit()
    await session.refresh(variant)
    return variant

async def delete_variant(
    variant_id: int,
    session: AsyncSession
):
    variant = await get_variant_by_id(variant_id, session)
    if not variant:
        raise ValueError("Variant not found")

    variant.is_active = False
    session.add(variant)
    await session.commit()

async def deduct_stock( #TODO only the paid one can remove this
    variant_id: int,
    quantity: int,
    session: AsyncSession
):

    # Lock row
    result = await session.exec(
        select(ProductVariant)
        .where(ProductVariant.id == variant_id)
        .with_for_update()
    )
    variant = result.first()

    if not variant:
        raise ValueError("Variant not found")

    if variant.stock < quantity:
        raise ValueError("Not enough stock")

    variant.stock -= quantity

    session.add(variant)
    await session.commit()
