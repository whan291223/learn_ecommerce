from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field
if TYPE_CHECKING:
    from .category_schema import CategoryPublic
    from .review_schema import ReviewPublic
    from .product_variant_schema import ProductVariantPublic


class ProductBase(SQLModel):
    name: str 
    description: str 
    

class ProductCreate(ProductBase):
    category_id: int
    image_path: Optional[str] = None

class ProductUpdate(ProductBase):
    id: int
    category_id: int
    image_path: Optional[str] = None

class ProductPublic(ProductBase):
    id: int
    category: "CategoryPublic"
    reviews: List["ReviewPublic"] = Field(default_factory=list)
    variants: List["ProductVariantPublic"] = Field(default_factory=list)
    image_path: Optional[str] = None

class ProductWithoutCategory(ProductBase):
    id: int
    reviews: List["ReviewPublic"] = Field(default_factory=list)
    image_path: Optional[str] = None

class ProductCategoryID(ProductBase):
    id: int
    category_id: int