import stripe
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import Product
from schema.payment_schema import CheckoutRequest

async def create_stripe_session(data: CheckoutRequest, session: AsyncSession, secret_key: str):
    stripe.api_key = secret_key
    
    # 1. Optimize: Get all IDs from the request
    product_ids = [item.product_id for item in data.items]
    
    # 2. Fetch all products in ONE query
    statement = select(Product).where(Product.id.in_(product_ids))
    result = await session.exec(statement)
    db_products = {p.id: p for p in result.all()}

    line_items = []
    for item in data.items:
        product = db_products.get(item.product_id)
        if product:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product.name},
                    "unit_amount": int(product.price * 100),
                },
                "quantity": item.quantity,
            })

    # 3. Create Stripe Session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
    )
    
    return checkout_session