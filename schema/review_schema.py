from sqlmodel import SQLModel

class ReviewBase(SQLModel):
    text: str
    rating: int

class ReviewCreate(ReviewBase):
    user_id: int
    product_id: int

class ReviewsOfProduct(ReviewBase):
    id: int
    user_id: int

class ReviewsOfUser(ReviewBase):
    id: int
    product_id: int

class ReviewPublic(ReviewBase):
    id: int
    user_id: int
    product_id: int