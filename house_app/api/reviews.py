from house_app.db.database import SessionLocale
from house_app.db.models import Review
from house_app.db.schemas import  ReviewSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends,APIRouter
from typing import List


reviews_router=APIRouter(prefix='/reviews',tags=['Reviews'])


async def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()

@reviews_router.post('/',response_model=ReviewSchema)
async def create_review(review:ReviewSchema,db:Session=Depends(get_db)):
    review =Review(review_name=review.review_name)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@reviews_router.get('/',response_model=List[ReviewSchema])
async def list_reviews(db:Session =Depends(get_db)):
    return db.query(Review).all()