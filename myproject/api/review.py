from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Review
from myproject.database.schema import ReviewInputSchema, ReviewOutSchema
from myproject.database.db import SessionLocal

review_router = APIRouter(prefix="/review", tags=["Review CRUD"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@review_router.post("/", response_model=ReviewOutSchema)
async def create_review(review: ReviewInputSchema, db: Session = Depends(get_db)):
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Рейтинг 1ден 5ке чейинки сан болушу керек")

    review_db = Review(**review.model_dump())
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return review_db


@review_router.get("/", response_model=List[ReviewOutSchema])
async def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@review_router.get("/{review_id}", response_model=ReviewOutSchema)
async def detail_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Сын-пикир табылган жок")
    return review


@review_router.put("/{review_id}", response_model=dict)
async def update_review(review_id: int, review_data: ReviewInputSchema, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Сын-пикир табылган жок")
    for key, value in review_data.model_dump().items():
        setattr(review_db, key, value)

    db.commit()
    db.refresh(review_db)
    return {"message": "Review updated"}


@review_router.delete("/{review_id}", response_model=dict)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review_db = db.query(Review).filter(Review.id == review_id).first()
    if not review_db:
        raise HTTPException(status_code=404, detail="Сын-пикир табылган жок")

    db.delete(review_db)
    db.commit()
    return {"message": "Review deleted"}
