from .user_schema import UserCreate, UserPublic, UserPublicWithoutReview
from .product_schema import ProductCreate, ProductPublic, ProductUpdate, ProductWithoutCategory
from .category_schema import CategoryCreate, CategoryPublic, CategoryWithProductPublic
from .review_schema import ReviewCreate, ReviewPublic, ReviewsOfUser

# Rebuild all schemas that have nested relationships
UserPublic.model_rebuild()
ProductPublic.model_rebuild()
ProductWithoutCategory.model_rebuild()
CategoryWithProductPublic.model_rebuild()

# Exporting them makes importing elsewhere much cleaner
__all__ = [
    "UserCreate", "UserPublic", "UserPublicWithoutReview",
    "ProductCreate", "ProductPublic", "ProductUpdate", "ProductWithoutCategory",
    "CategoryCreate", "CategoryPublic", "CategoryWithProductPublic",
    "ReviewCreate", "ReviewPublic", "ReviewsOfUser"
]