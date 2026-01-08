from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .product_schema import ProductWithoutCategory

class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int

class CategoryWithProductPublic(CategoryBase):
    id: int
    products: List["ProductWithoutCategory"] = Field(default_factory=list)