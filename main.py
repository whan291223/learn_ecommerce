from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api import user, product, category, review, payment

app = FastAPI()

app.include_router(user.router, prefix="/api/v1")
app.include_router(product.router, prefix="/api/v1")
app.include_router(category.router, prefix="/api/v1")
app.include_router(review.router, prefix="/api/v1")
app.include_router(payment.router, prefix="/api/v1")

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

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

@app.get("/", tags=["Root"])
def read_root():
    """
    A simple root endpint to confirm that api is running
    """

    return { "message" : "Welcome to E-commerve API"}