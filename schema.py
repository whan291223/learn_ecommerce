# between database and api there should be a schema which is the filter
# or the process between the two like hashing a password send via api

# represent how data is sent or received via api (What user and client) see
# z



from typing import List, Optional
from sqlmodel import SQLModel

class CategoryBase(SQLModel):
    pass

class CategoryCreate(SQLModel):
    pass

class CategoryPublic(SQLModel):
    pass

class UserBase(SQLModel):
    pass

class UserCreate(SQLModel):
    pass

class UserPublic(SQLModel):
    pass

class ReviewBase(SQLModel):
    pass

class ReviewCreate(SQLModel):
    pass

class ReviewPublic(SQLModel):
    pass

class ProductBase(SQLModel): # didn't use table = True because we didn't want to create the table we need only mediump between database
    name: str 
    description: str 
    price: float

class ProductCreate(ProductBase): #when product is create it create in some category
    category_id: int

class ProductPublic(ProductBase): #the product that shown on page should contain id which contain data of product, category, list of review
    id: int
    category: CategoryPublic
    review: List[ReviewPublic] = []