from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
from models import Base, Category, Item
from schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
    ItemCreate,
    ItemUpdate,
    ItemResponse,
)

app = FastAPI()

# -------------------------
# Create DB tables
# -------------------------
Base.metadata.create_all(bind=engine)


# -------------------------
# Root
# -------------------------
@app.get("/")
def root():
    return {"message": "FastAPI backend running"}


# =====================================================
# CATEGORY APIs (DAY 2)
# =====================================================

@app.post("/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):

    if category.parent_id is not None:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category does not exist")

    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")

    if category.parent_id == category_id:
        raise HTTPException(
            status_code=400, detail="Category cannot be parent of itself"
        )

    if category.parent_id is not None:
        parent = db.query(Category).filter(Category.id == category.parent_id).first()
        if not parent:
            raise HTTPException(status_code=400, detail="Parent category does not exist")

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    child = db.query(Category).filter(Category.parent_id == category_id).first()
    if child:
        raise HTTPException(
            status_code=400,
            detail="Category has subcategories and cannot be deleted",
        )

    item_exists = db.query(Item).filter(Item.category_id == category_id).first()
    if item_exists:
        raise HTTPException(
            status_code=400,
            detail="Category has items and cannot be deleted",
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}


# =====================================================
# ITEM APIs (DAY 3)
# =====================================================

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):

    category = db.query(Category).filter(Category.id == item.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    sku_exists = db.query(Item).filter(Item.sku == item.sku).first()
    if sku_exists:
        raise HTTPException(status_code=400, detail="SKU already exists")

    new_item = Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/items", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.category_id is not None:
        category = db.query(Category).filter(Category.id == item.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")

    for key, value in item.dict(exclude_unset=True).items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}
