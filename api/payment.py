import stripe
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from core.config import settings

router = APIRouter(prefix="/payment", tags=["Payment"])

stripe.api_key = settings.STRIPE_SECRET_KEY


# ----- Schemas -----
class CartItem(BaseModel):
    name: str
    price: float
    quantity: int


class CheckoutRequest(BaseModel):
    items: List[CartItem]


# ----- Route -----
@router.post("/create-checkout-session")
def create_checkout_session(data: CheckoutRequest):
    line_items = []

    for item in data.items:
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.name,
                },
                "unit_amount": int(item.price * 100),  # cents
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
