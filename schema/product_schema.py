from typing import List, Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .category_schema import CategoryPublic
    from .review_schema import ReviewPublic

class ProductBase(SQLModel):
    name: str 
    description: str 
    price: float

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
    image_path: Optional[str] = None

class ProductWithoutCategory(ProductBase):
    id: int
    reviews: List["ReviewPublic"] = Field(default_factory=list)
    image_path: Optional[str] = None

class ProductCategoryID(ProductBase):
    id: int
    category_id: int