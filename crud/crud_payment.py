import stripe
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import Product, Order, OrderItem
from schema.payment_schema import CheckoutRequest

async def create_stripe_session(
    data: CheckoutRequest,
    session: AsyncSession,
    secret_key: str
):
    stripe.api_key = secret_key

    # 1. Fetch products
    product_ids = [item.product_id for item in data.items]
    statement = select(Product).where(Product.id.in_(product_ids))
    result = await session.exec(statement)
    db_products = {p.id: p for p in result.all()}

    line_items = []
    total_price_baths = 0

    # 2. Create Order (PENDING)
    order = Order(
        user_id=data.user_id,
        status="pending",
        total_price_baths=0  # temp
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)

    # 3. Create OrderItems + Stripe line items
    for item in data.items:
        product = db_products.get(item.product_id)
        if not product:
            raise ValueError("Invalid product")

        price_baths = int(product.price * 100)
        total_price_baths += price_baths * item.quantity

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price_at_purchase_baths=price_baths
        )
        session.add(order_item)

        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {"name": product.name},
                "unit_amount": price_baths,
            },
            "quantity": item.quantity,
        })

    # 4. Update order total
    order.total_price_baths = total_price_baths
    session.add(order)
    await session.commit()

    # 5. Create Stripe Checkout Session
    stripe_session = await stripe.checkout.Session.create_async(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:5173/cancel",
        metadata={
            "order_id": str(order.id),
            "user_id": str(data.user_id),
        }
    )
    order.stripe_session_id = stripe_session.id
    session.add(order)
    await session.commit() 

    return stripe_session


async def fulfill_order(session_data: dict, db: AsyncSession):
    # Stripe safety check
    if session_data.get("payment_status") != "paid":
        return

    metadata = session_data.get("metadata", {})
    order_id = metadata.get("order_id")

    if not order_id:
        return

    statement = select(Order).where(Order.id == int(order_id))
    result = await db.exec(statement)
    order = result.first()

    # Idempotency protection
    if not order or order.status == "paid":
        return

    # Only update the status - stripe_session_id is already set
    order.status = "paid"
    
    db.add(order)
    await db.commit()

    print(f"✅ Order {order_id} marked as PAID")

async def get_order_by_stripe_session(
    db: AsyncSession,
    session_id: str
) -> Order | None:
    statement = select(Order).where(Order.stripe_session_id == session_id)
    result = await db.exec(statement)
    return result.first()