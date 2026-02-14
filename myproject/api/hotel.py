from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from myproject.database.models import Hotel
from myproject.database.schema import HotelInputSchema, HotelOutSchema
from myproject.database.db import SessionLocal

hotel_router = APIRouter(prefix='/hotel', tags=['Hotel CRUD'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@hotel_router.post('/', response_model=HotelOutSchema)
async def create_hotel(hotel: HotelInputSchema, db: Session = Depends(get_db)):
    hotel_db = Hotel(**hotel.dict())
    db.add(hotel_db)
    db.commit()
    db.refresh(hotel_db)
    return hotel_db



@hotel_router.get('/', response_model=List[HotelOutSchema])
async def list_hotel(db: Session = Depends(get_db)):
    return db.query(Hotel).all()


@hotel_router.get('/{hotel_id}', response_model=HotelOutSchema)
async def detail_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail='Hotel not found')
    return hotel


@hotel_router.put('/{hotel_id}', response_model=dict)
async def update_hotel(hotel_id: int, hotel_: HotelInputSchema,
                       db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail='Hotel not found')

    for key, value in hotel_.dict().items():
        setattr(hotel_db, key, value)

    db.commit()
    db.refresh(hotel_db)
    return {"message": "Hotel updated"}


@hotel_router.delete('/{hotel_id}', response_model=dict)
async def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel_db = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel_db:
        raise HTTPException(status_code=404, detail='Hotel not found')

    db.delete(hotel_db)
    db.commit()
    return {"message": "Hotel deleted"}

