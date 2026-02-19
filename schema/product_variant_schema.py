from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .product_schema import ProductPublic

class ProductVariantBase(SQLModel):
    option1_name: Optional[str] = None
    option1_value: Optional[str] = None
    option2_name: Optional[str] = None
    option2_value: Optional[str] = None
    is_active: bool = True
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