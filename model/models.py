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
    
    category: "Category" = Relationship(back_populates="product")
    reviews: List["Review"] = Relationship(back_populates="product")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    
    product_id: int = Field(foreign_key="product.id")
    products: List["Product"] = Relationship(back_populates="category")


class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    rating: int
    
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="review")
    
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="review")