from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from core.db import get_session
from model.models import Order, OrderItem, User, Product, OrderStatus
from datetime import datetime, timezone
from core.auth import is_customer, is_admin, get_current_user
from typing import Annotated

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
async def get_all_orders(
    session: AsyncSession = Depends(get_session)
):
    """Get all orders with user and items"""
    statement = select(Order).order_by(Order.id.desc())
    result = await session.exec(statement)
    orders = result.all()
    
    # Fetch related data
    orders_data = []
    for order in orders:
        # Get user
        user_stmt = select(User).where(User.id == order.user_id)
        user_result = await session.exec(user_stmt)
        user = user_result.first()
        
        # Get order items with product names
        items_stmt = select(OrderItem).where(OrderItem.order_id == order.id)
        items_result = await session.exec(items_stmt)
        items = items_result.all()
        
        # Fetch product details for each item
        items_data = []
        for item in items:
            product_stmt = select(Product).where(Product.id == item.product_variant_id)
            product_result = await session.exec(product_stmt)
            product = product_result.first()
            
            items_data.append({
                "product_id": item.product_variant_id,
                "product_name": product.name if product else f"Product #{item.product_variant_id}",
                "quantity": item.quantity,
                "price_at_purchase_bahts": item.price_at_purchase_bahts
            })
        
        orders_data.append({
            "id": order.id,
            "user_id": order.user_id,
            "username": user.username if user else None,
            "total_price_bahts": order.total_price_bahts,
            "status": order.status,
            "stripe_session_id": order.stripe_session_id,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "updated_at": order.updated_at.isoformat() if order.updated_at else None,
            "items": items_data
        })
    
    return orders_data

@router.patch("/{order_id}/status")
async def update_order_status(
    order_id: int,
    new_status: OrderStatus,
    current_user: Annotated[User, Depends(is_admin())],
    session: AsyncSession = Depends(get_session)
):
    """Update order status (shipped, delivered, etc.)"""
    statement = select(Order).where(Order.id == order_id)
    result = await session.exec(statement)
    order = result.first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order.status = new_status
    order.updated_at = datetime.now(timezone.utc)
    
    session.add(order)
    await session.commit()
    
    return {"success": True, "order_id": order_id, "new_status": new_status}