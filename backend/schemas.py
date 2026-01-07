from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
