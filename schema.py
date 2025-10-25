# between database and api there should be a schema which is the filter
# or the process between the two like hashing a password send via api

# represent how data is sent or received via api (What user and client) see
# z



from typing import List, Optional
from sqlmodel import SQLModel

class CategoryBase(SQLModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int
    products: List["ProductPublic"]

class UserBase(SQLModel):
    username: str

class UserCreate(UserBase): # use when create User
    password: str
    role: str

class UserPublic(UserBase): # what public will see
    id: int
    role: str
    reviews: List["ReviewPublic"]

class ReviewBase(SQLModel):
    text: str
    rating: int

class ReviewCreate(ReviewBase):
    user_id: int
    product_id: int
    
class ReviewPublic(ReviewBase):
    id: int
    user: UserPublic
    product: ProductPublic

class ProductBase(SQLModel): # didn't use table = True because we didn't want to create the table we need only mediump between database
    name: str 
    description: str 
    price: float

class ProductCreate(ProductBase): #when product is create it create in some category
    category_id: int

class ProductPublic(ProductBase): #the product that shown on page should contain id which contain data of product, category, list of review
    id: int
    category: CategoryPublic
    review: List["ReviewPublic"] = []

CategoryPublic.model_rebuild()
ProductPublic.model_rebuild()
UserPublic.model_rebuild()
ReviewPublic.model_rebuild()