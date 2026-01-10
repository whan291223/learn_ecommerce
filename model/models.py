""" 

Learn from clip 7a
SQLModel = SQLAlchemy + Pydantic


before you code the library name you should know why you using them!!

sqlmodel[aync] -> This is for writing our models with async/await
asyncpg-stubs -> database driver with inline type hints
alembic -> version control for database
psycopg2-binary: synchronous Python driver for postgressql -> 
"""

from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    role: str = "customer"
    
    reviews: List["Review"] = Relationship(back_populates="user")
    
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str 
    price: float
    image_path: str|None = None
    category_id: int = Field(foreign_key="category.id")
    category: Category = Relationship(back_populates="products")
    reviews: List["Review"] = Relationship(back_populates="product")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    products: List["Product"] = Relationship(back_populates="category")



class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    rating: int
    
    user_id: int = Field(foreign_key="user.id") #reviews belond to user therefore it should have foreigh key here
    user: User = Relationship(back_populates="reviews")
    
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="reviews")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    total_price_baths: int
    status: str = "pending"

    stripe_session_id: Optional[str] = Field(default=None, index=True, unique=True)

    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")

    product_id: int = Field(foreign_key="product.id")
    quantity: int
    price_at_purchase_baths: int

    order: Optional[Order] = Relationship(back_populates="items")