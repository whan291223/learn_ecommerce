from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from core.db import get_session
from crud import crud_category
from schema import CategoryCreate, CategoryPublic

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=CategoryPublic
             
             )