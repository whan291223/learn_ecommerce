from sqlmodel import SQLModel
from typing import List

class CartItem(SQLModel):
    product_variant_id: int
    quantity: int


class CheckoutRequest(SQLModel):
    items: List[CartItem]
