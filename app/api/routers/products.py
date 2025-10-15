from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.products import (
    ProductCreate, ProductOut, ProductUpdate,
    CategoryCreate, CategoryOut, ProductTagCreate, ProductTagOut
)
from app.crud import products as crud
from app.core.database import get_db

router = APIRouter()

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/", response_model=List[ProductOut])
def list_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_all_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product_data)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category.name, category.description)

@router.get("/categories", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)

@router.post("/tags", response_model=ProductTagOut, status_code=status.HTTP_201_CREATED)
def create_tag(tag: ProductTagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db, tag.name)

@router.get("/tags", response_model=List[ProductTagOut])
def list_tags(db: Session = Depends(get_db)):
    return crud.get_all_tags(db)
