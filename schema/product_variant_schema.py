from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .product_schema import ProductPublic

class ProductVariantBase(SQLModel):
    color: Optional[str] = None
    size: Optional[str] = None
    price: float
    stock: int

class ProductVariantCreate(ProductVariantBase):
    product_id: int

class ProductVariantUpdate(ProductVariantBase):
    id: int
    product_id: int

class ProductVariantPublic(ProductVariantBase):
    id: int
    product_id: int

class ProductVariantWithProduct(ProductVariantBase):
    id: int
    product_id: int
    product: "ProductPublic"