from fastapi import FastAPI
from database import get_db
from models import Category
from sqlalchemy.orm import Session
from typing import List
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse
app = FastAPI()



@app.get("/")
def root():
    return {"Message":"fastAPI backend running"}




from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db, engine
from models import Category, Base
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FastAPI backend running"}


# -------------------------
# Create Category
# -------------------------
@app.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    # Validate parent category
    if category.parent_id is not None:
        parent = db.query(Category).filter(
            Category.id == category.parent_id
        ).first()
        if not parent:
            raise HTTPException(
                status_code=400,
                detail="Parent category does not exist"
            )

    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


# -------------------------
# Get All Categories
# -------------------------
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# -------------------------
# Update Category
# -------------------------
@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    db_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Prevent self-parenting
    if category.parent_id == category_id:
        raise HTTPException(
            status_code=400,
            detail="Category cannot be parent of itself"
        )

    # Validate parent category
    if category.parent_id is not None:
        parent = db.query(Category).filter(
            Category.id == category.parent_id
        ).first()
        if not parent:
            raise HTTPException(
                status_code=400,
                detail="Parent category does not exist"
            )

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category


# -------------------------
# Delete Category
# -------------------------
@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    # Check for child categories
    child = db.query(Category).filter(
        Category.parent_id == category_id
    ).first()
    if child:
        raise HTTPException(
            status_code=400,
            detail="Category has subcategories and cannot be deleted"
        )

    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}
