from fastapi import APIRouter, Depends, HTTPException
from core.config import settings
from core.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from schema.payment_schema import CheckoutRequest
from crud.crud_payment import create_stripe_session  # Import your new function

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/create-checkout-session")
async def create_checkout_session(
    data: CheckoutRequest,
    session: AsyncSession = Depends(get_session)
):
    try:
        checkout_session = await create_stripe_session(
            data=data, 
            session=session, 
            secret_key=settings.STRIPE_SECRET_KEY
        )
        return {"url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))