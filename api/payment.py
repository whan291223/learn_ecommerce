# The Logic Flow
# To make this work correctly with your existing setup, you should change your Router logic to follow this sequence:
# Frontend sends the list of items to /create-checkout-session.
# FastAPI calculates the total price and creates an Order record with status="pending".
# FastAPI then calls create_stripe_session and passes that new order.id into the Stripe metadata.
# Stripe handles the payment.

# Webhook receives the order_id and updates that specific order to "paid".
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from core.config import settings
from core.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from schema.payment_schema import CheckoutRequest
from crud.crud_payment import create_stripe_session, fulfill_order, get_order_by_stripe_session  # Import your new function
from core.config import settings
import stripe
from model.models import OrderStatus
from datetime import datetime, timezone
from core.auth import get_current_user
from typing import Annotated
from model.models import User
router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/create-checkout-session")
async def create_checkout_session(
    data: CheckoutRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session)
):
    try:
        checkout_session = await create_stripe_session(
            data=data,
            current_user=current_user,  # 👈 pass user explicitly
            session=session,
            secret_key=settings.STRIPE_SECRET_KEY
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/webhook")
async def stripe_webhook(
    request: Request, 
    stripe_signature: str = Header(None, alias="Stripe-Signature"),
    db: AsyncSession = Depends(get_session)
):
    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Webhook Signature")
    print(event['type'])
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session_data = event['data']['object']
        # Call the CRUD function
        await fulfill_order(session_data, db)
    if event["type"] == "checkout.session.expired": # TODO expired still not work
        session_data = event["data"]["object"]
        print("the session is expiered")
        order = await get_order_by_stripe_session(db, session_data["id"])
        if order and order.status == OrderStatus.pending:
            order.status = OrderStatus.expired
            order.expired_at = datetime.now(timezone.utc)
            db.add(order)
            await db.commit()
    return {"status": "success"}
    

@router.get("/checkout-status")
async def checkout_status(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    order = await get_order_by_stripe_session(db, session_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order.id,
        "status": order.status,
        "total_price": order.total_price_bahts
    }
