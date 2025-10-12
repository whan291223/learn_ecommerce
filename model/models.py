from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str
    
    reviews: List["Review"] = Relationship(back_populates="user")
    role: str = "customer"
    
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str 
    
    category: "Category" = Relationship(back_populates="product")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Review(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
