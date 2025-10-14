from pydantic import BaseModel, Field
from typing import Optional, List


# --- Category Schemas ---
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    class Config:
        orm_mode = True


# --- Product Tag Schemas ---
class ProductTagBase(BaseModel):
    name: str

class ProductTagCreate(ProductTagBase):
    pass

class ProductTagOut(ProductTagBase):
    id: int
    class Config:
        orm_mode = True


# --- Product Image Schemas ---
class ProductImageBase(BaseModel):
    image_url: str
    is_primary: Optional[bool] = False

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageOut(ProductImageBase):
    id: int
    class Config:
        orm_mode = True


# --- Product Schemas ---
class ProductBase(BaseModel):
    name: str = Field(..., example="Wireless Mouse")
    description: Optional[str] = Field(None, example="Ergonomic wireless mouse with 2.4GHz USB receiver")
    price: float = Field(..., example=999.99)
    stock: int = Field(..., example=50)
    gst_percentage: float = Field(..., example=18.0)

class ProductCreate(ProductBase):
    category_id: int
    tag_ids: Optional[List[int]] = []
    images: Optional[List[ProductImageCreate]] = []

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    gst_percentage: Optional[float]
    category_id: Optional[int]
    tag_ids: Optional[List[int]] = []
    images: Optional[List[ProductImageCreate]] = []

class ProductOut(ProductBase):
    id: int
    category: Optional[CategoryOut]
    tags: Optional[List[ProductTagOut]]
    images: Optional[List[ProductImageOut]]

    model_config = {
        "from_attributes": True
    }

