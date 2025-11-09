from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import user, product, category, review

app = FastAPI()

app.include_router(user.router, prefix="/api/v1")
app.include_router(product.router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")
app.include_router(review.router, prefix="/api/v1")

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpint to confirm that api is running
    """

    return { "message" : "Welcome to E-commerve API"}