from fastapi import FastAPI
from api import user, product, category, review

app = FastAPI()

app.include_router(user.router, prefix="/api/v1")
app.include_router(product.router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")
app.include_router(review.router, prefix="/api/v1")