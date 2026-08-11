from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from myproject.database.models import Booking
from myproject.database.schema import BookingInputSchema, BookingOutSchema
from myproject.database.db import SessionLocal

booking_router = APIRouter(prefix="/booking", tags=["Booking CRUD"])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@booking_router.post("/", response_model=BookingOutSchema)
async def create_booking(booking: BookingInputSchema, db: Session = Depends(get_db)):
    if booking.check_out <= booking.check_in:
        raise HTTPException(status_code=400, detail="Check-out датасы check-in датасынан кийин болушу керек")

    booking_db = Booking(**booking.model_dump())
    db.add(booking_db)
    db.commit()
    db.refresh(booking_db)
    return booking_db


@booking_router.get("/", response_model=List[BookingOutSchema])
async def list_bookings(db: Session = Depends(get_db)):
    return db.query(Booking).all()


@booking_router.get("/{booking_id}", response_model=BookingOutSchema)
async def detail_booking(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронь табылган жок")
    return booking


@booking_router.put("/{booking_id}", response_model=dict)
async def update_booking(booking_id: int, booking_data: BookingInputSchema, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Бронь табылган жок")

    for key, value in booking_data.model_dump().items():
        setattr(booking_db, key, value)

    db.commit()
    db.refresh(booking_db)
    return {"message": "Бронь ийгиликтүү жаңыртылды"}


@booking_router.delete("/{booking_id}", response_model=dict)
async def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    booking_db = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking_db:
        raise HTTPException(status_code=404, detail="Бронь табылган жок")

    db.delete(booking_db)
    db.commit()
    return {"message": "Бронь өчүрүлдү"}
