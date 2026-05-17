from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from .product_schema import ProductVariantPublic

class OrderItemPublic(SQLModel):
    product_variant_id: int
    quantity: int
    price_at_purchase_bahts: float
    product_variant: Optional[ProductVariantPublic] = None