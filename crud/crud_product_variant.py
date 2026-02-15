from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import ProductVariant, Product


async def create_variant(
    product_id: int,
    color: str | None,
    size: str | None,
    price_bahts: int,
    stock: int,
    session: AsyncSession
) -> ProductVariant:
    
    # Make sure product exists
    result = await session.exec(select(Product).where(Product.id == product_id))
    product = result.first()
    if not product:
        raise ValueError("Product not found")

    variant = ProductVariant(
        product_id=product_id,
        color=color,
        size=size,
        price_bahts=price_bahts,
        stock=stock
    )

    session.add(variant)
    await session.commit()
    await session.refresh(variant)
    return variant


async def get_all_variants(
    session: AsyncSession
) -> list[ProductVariant]:

    result = await session.exec(
        select(ProductVariant)
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
        select(ProductVariant).where(ProductVariant.product_id == product_id)
    )
    return result.all()

async def update_variant(
    variant_id: int,
    color: str | None,
    size: str | None,
    price_bahts: int,
    stock: int,
    session: AsyncSession
) -> ProductVariant:

    variant = await get_variant_by_id(variant_id, session)
    if not variant:
        raise ValueError("Variant not found")

    variant.color = color
    variant.size = size
    variant.price_bahts = price_bahts
    variant.stock = stock

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

    await session.delete(variant)
    await session.commit()