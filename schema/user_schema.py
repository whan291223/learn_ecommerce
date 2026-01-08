from typing import List, TYPE_CHECKING
from sqlmodel import SQLModel, Field

if TYPE_CHECKING:
    from .review_schema import ReviewsOfUser

class UserBase(SQLModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str

class UserPublic(UserBase):
    id: int
    role: str
    reviews: List["ReviewsOfUser"] = Field(default_factory=list)

class UserPublicWithoutReview(UserBase):
    id: int
    role: str