from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from myproject.database.models import HotelImage
from myproject.database.schema import HotelImageInputSchema, HotelImageOutSchema
from myproject.database.db import SessionLocal

hotel_image_router = APIRouter(prefix='/hotel-image', tags=['Hotel Image CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_image_router.post('/', response_model=HotelImageOutSchema)
async def create_hotel_image(image: HotelImageInputSchema, db: Session = Depends(get_db)):
    image_db = HotelImage(**image.dict())
    db.add(image_db)
    db.commit()
    db.refresh(image_db)
    return image_db


@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def list_hotel_images(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()



@hotel_image_router.get('/{image_id}', response_model=HotelImageOutSchema)
async def detail_hotel_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail='Hotel image not found')
    return image


@hotel_image_router.put('/{image_id}', response_model=dict)
async def update_hotel_image(image_id: int, image_: HotelImageInputSchema,
                             db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Hotel image not found')

    for key, value in image_.dict().items():
        setattr(image_db, key, value)

    db.commit()
    db.refresh(image_db)
    return {"message": "Hotel image updated"}


@hotel_image_router.delete('/{image_id}', response_model=dict)
async def delete_hotel_image(image_id: int, db: Session = Depends(get_db)):
    image_db = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not image_db:
        raise HTTPException(status_code=404, detail='Hotel image not found')

    db.delete(image_db)
    db.commit()
    return {"message": "Hotel image deleted"}