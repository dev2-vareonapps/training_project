from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    sku: str
    category_id: int
    price: float | None = None
    quantity: int | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = None
from pydantic import BaseModel
from typing import Optional


# =========================
# CATEGORY SCHEMAS (DAY 2)
# =========================

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


# =========================
# ITEM SCHEMAS (DAY 3)
# =========================

class ItemBase(BaseModel):
    name: str
    sku: str
    category_id: int
    price: Optional[float] = None
    quantity: Optional[int] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_active: Optional[bool] = None


class ItemResponse(ItemBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
    category_id: int | None = None
    price: float | None = None
    quantity: int | None = None
    is_active: bool | None = None

class ItemResponse(ItemBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

