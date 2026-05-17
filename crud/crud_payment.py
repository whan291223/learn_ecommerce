import stripe
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import ProductVariant, Order, OrderItem
from schema.payment_schema import CheckoutRequest
from datetime import datetime, timezone
from model.models import User
from fastapi import HTTPException


async def create_stripe_session(
    data: CheckoutRequest,
    current_user: User,
    session: AsyncSession,
    secret_key: str
):
    stripe.api_key = secret_key

    # 1. Fetch product variants (not products)
    variant_ids = [item.product_variant_id for item in data.items]
    statement = select(ProductVariant).where(ProductVariant.id.in_(variant_ids))
    result = await session.exec(statement)
    db_variants = {v.id: v for v in result.all()}

    # 2. Validate all variants exist and are active
    for item in data.items:
        variant = db_variants.get(item.product_variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail=f"Variant {item.product_variant_id} not found")
        if not variant.is_active:
            raise HTTPException(status_code=400, detail=f"Variant {item.product_variant_id} is no longer available")
        if variant.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for variant {item.product_variant_id}")

    # 3. Create Order (PENDING)
    order = Order(
        user_id=current_user.id,
        status="pending",
        total_price_bahts=0  # updated below
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    # 4. Create OrderItems + Stripe line items
    line_items = []
    total_price_bahts = 0

    for item in data.items:
        variant = db_variants[item.product_variant_id]

        price_bahts = int(variant.price)
        price_satangs = price_bahts * 100
        total_price_bahts += price_bahts * item.quantity

        # Build a readable product name including variant options
        option_label = " / ".join(filter(None, [
            variant.option1_value,
            variant.option2_value,
        ]))
        display_name = f"Variant #{variant.id}" + (f" ({option_label})" if option_label else "")

        order_item = OrderItem(
            order_id=order.id,
            product_variant_id=variant.id,
            quantity=item.quantity,
            price_at_purchase_bahts=price_bahts
        )
        session.add(order_item)

        line_items.append({
            "price_data": {
                "currency": "thb",
                "product_data": {"name": display_name},
                "unit_amount": price_satangs,
            },
            "quantity": item.quantity,
        })

    # 5. Update order total
    order.total_price_bahts = total_price_bahts
    session.add(order)
    await session.commit()

    # 6. Create Stripe Checkout Session
    try:
        stripe_session = await stripe.checkout.Session.create_async(
            payment_method_types=["card", "promptpay"],
            mode="payment",
            line_items=line_items,
            success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:5173/cancel",
            metadata={
                "order_id": str(order.id),
                "user_id": str(current_user.id),
            }
        )
        order.stripe_session_id = stripe_session.id
        session.add(order)
        await session.commit()

        return stripe_session

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e.user_message))


async def fulfill_order(session_data: dict, db: AsyncSession):
    if session_data.get("payment_status") != "paid":
        return

    metadata = session_data.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        return

    statement = select(Order).where(Order.id == int(order_id))
    result = await db.exec(statement)
    order = result.first()

    if not order or order.status == "paid":
        return

    order.status = "paid"
    order.updated_at = datetime.now(timezone.utc)

    db.add(order)
    await db.commit()


async def get_order_by_stripe_session(
    db: AsyncSession,
    session_id: str
) -> Order | None:
    statement = select(Order).where(Order.stripe_session_id == session_id)
    result = await db.exec(statement)
    return result.first()