import stripe
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from core.config import settings
from core.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from model.models import Product
#TODO Resturcture this
router = APIRouter(prefix="/payment", tags=["Payment"])

stripe.api_key = settings.STRIPE_SECRET_KEY


# ----- Schemas -----
class CartItem(BaseModel):
    product_id: int
    quantity: int


class CheckoutRequest(BaseModel):
    items: List[CartItem]


# ----- Route -----
@router.post("/create-checkout-session")
async def create_checkout_session(
    data: CheckoutRequest,
    session: AsyncSession = Depends(get_session)
):
    line_items = []

    for item in data.items:
        statement = select(Product).where(Product.id == item.product_id)
        result = await session.exec(statement)
        product = result.first()
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": product.name,
                },
                "unit_amount": int(product.price * 100),  # cents
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
    )

    return {"url": session.url}
