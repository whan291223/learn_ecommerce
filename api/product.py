from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form, File
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.db import get_session
from core.auth import get_current_user
from model.models import User
from crud import crud_product
from schema.product_schema import ProductCreate, ProductPublic, ProductCategoryID, ProductUpdate
from schema.review_schema import ReviewPublic
import uuid, os #fix if user upload two image file with the same name

router = APIRouter(prefix="/products", tags=["product"]) # router will initiate path for api automaticly
#  ex. .post('product/xyz') -> .post('xyz')

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductCategoryID)
async def create_new_product(
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile|None = File(None),
    session: AsyncSession = Depends(get_session)
) -> ProductCategoryID: #fix add default factoty field for reviews, and use differrent schema for show only category_id
    """Need to change the ProductCrete to multiform so that it can 

    Raises:
        HTTPException: _description_

    Returns:
        ProductCategoryID: _description_
    """
    try:
        image_path = None
        if image:
            os.makedirs("static/images", exist_ok=True)
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            image_path = f"static/images/{filename}"

            with open(image_path, "wb") as f:
                f.write(await image.read())
        product_data = ProductCreate(
            name=name,
            description=description,
            category_id=category_id,
            image_path=image_path
        )
        new_product = await crud_product.create_product(product_data=product_data, session=session)
        return new_product
    except IntegrityError as integrity_error:
        if hasattr(integrity_error.orig, "diag") and getattr(integrity_error.orig.diag, "message_detail", None):
            detail = integrity_error.orig.diag.message_detail
        else:
            detail = str(integrity_error.orig)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

@router.get("/", response_model=List[ProductPublic])
# , dependencies=[Depends(get_current_user)])
async def get_all_product(
    session: AsyncSession = Depends(get_session)
) -> List[ProductPublic]:
    products = await crud_product.get_all_product(session=session)
    return products

@router.get("/{product_id}", response_model=ProductPublic)
async def get_product_detail(
    product_id: int,
    session: AsyncSession = Depends(get_session)
) -> ProductPublic:
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found!")
    return product

@router.get("/{product_id}/reviews", response_model=List[ReviewPublic])
async def get_product_reviews(
    product_id: int,
    session: AsyncSession = Depends(get_session)
) -> List[ReviewPublic]:
    product = await crud_product.get_product_by_id(product_id=product_id, session=session)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {product_id} not found!")

    return product.reviews

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    try:
        await crud_product.delete_product(product_id=product_id, session=session)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Product id: {product_id} not found")

@router.put("/", response_model=ProductCategoryID)
async def update_product(
    id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile|None = File(None),
    session: AsyncSession = Depends(get_session)
) -> ProductCategoryID:
    try:
        image_path = None
        if image:
            os.makedirs("static/images", exist_ok=True)
            ext = os.path.splitext(image.filename)[1]
            filename = f"{uuid.uuid4()}{ext}"
            image_path = f"static/images/{filename}"

            with open(image_path, "wb") as f:
                f.write(await image.read())

        product_data = ProductUpdate(
            id = id,
            name = name,
            description = description,
            category_id = category_id,
            image_path=image_path
        )
        product = await crud_product.update_product(product_data=product_data, session=session)
        return product
    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Product id: {product_data.id} not found")
    except IntegrityError as intergrity_error:
        if hasattr(intergrity_error.orig, "diag") and getattr(intergrity_error.orig.diag, "message_detail", None):
            detail = intergrity_error.orig.diag.message_detail
        else:
            detail = str(intergrity_error.orig)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
        



# except IntegrityError as integrity_error:
#         if hasattr(integrity_error.orig, "diag") and getattr(integrity_error.orig.diag, "message_detail", None):
#             detail = integrity_error.orig.diag.message_detail
#         else:
#             detail = str(integrity_error.orig)
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
